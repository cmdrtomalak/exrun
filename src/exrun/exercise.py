"""Exercise metadata parsing."""

import tomllib
from pathlib import Path

from exrun.models import CourseConfig, Exercise, ExerciseConfig, ProjectConfig


def find_config_file(start_path: Path | None = None) -> Path | None:
    """Find .exrun.toml by searching upward from start_path."""
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()
    home = Path.home()

    while current != current.parent:
        config_path = current / ".exrun.toml"
        if config_path.exists():
            return config_path
        if current == home:
            break
        current = current.parent

    global_config = home / ".config" / "exrun" / "config.toml"
    if global_config.exists():
        return global_config

    return None


def load_project_config(config_path: Path) -> ProjectConfig:
    """Load project configuration from .exrun.toml."""
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    project = data.get("project", {})
    defaults = data.get("defaults", {})

    exercises_path_str = project.get("exercises_path", "./exercises")
    if exercises_path_str.startswith(("http://", "https://", "git@")):
        raise NotImplementedError("Remote exercise fetching not yet supported")

    exercises_path = Path(exercises_path_str)
    if not exercises_path.is_absolute():
        exercises_path = config_path.parent / exercises_path

    return ProjectConfig(
        exercises_path=exercises_path.resolve(),
        default_language=defaults.get("language", "python"),
        default_test_runner=defaults.get("test_runner", "pytest"),
    )


def load_course_config(exercises_path: Path) -> CourseConfig:
    """Load course configuration from exercises.toml."""
    config_path = exercises_path / "exercises.toml"
    if not config_path.exists():
        return CourseConfig(name="Unnamed Course")

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    course = data.get("course", {})
    settings = data.get("settings", {})

    return CourseConfig(
        name=course.get("name", "Unnamed Course"),
        version=course.get("version", "1.0.0"),
        language=course.get("language", "python"),
        test_runner=course.get("test_runner", "pytest"),
        show_hints=settings.get("show_hints", True),
        max_attempts_before_hint=settings.get("max_attempts_before_hint", 3),
    )


def load_exercise_config(exercise_path: Path) -> ExerciseConfig:
    """Load exercise configuration from exercise.toml."""
    config_path = exercise_path / "exercise.toml"
    if not config_path.exists():
        return ExerciseConfig(
            name=exercise_path.name,
            order=_extract_order_from_name(exercise_path.name),
        )

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    exercise = data.get("exercise", {})
    test = data.get("test", {})
    hints = data.get("hints", {})

    return ExerciseConfig(
        name=exercise.get("name", exercise_path.name),
        order=exercise.get("order", _extract_order_from_name(exercise_path.name)),
        difficulty=exercise.get("difficulty", "beginner"),
        test_command=test.get("command"),
        timeout_seconds=test.get("timeout_seconds", 30),
        hints=hints.get("hints", []),
        hints_enabled=hints.get("enabled", True),
    )


def _extract_order_from_name(name: str) -> int:
    """Extract order number from exercise directory name like '01_variables'."""
    parts = name.split("_", 1)
    if parts and parts[0].isdigit():
        return int(parts[0])
    return 999


def load_exercise(exercise_path: Path) -> Exercise:
    """Load a complete exercise from its directory."""
    config = load_exercise_config(exercise_path)

    problem_path = exercise_path / "problem.md"
    problem_md = ""
    if problem_path.exists():
        problem_md = problem_path.read_text()

    return Exercise(
        path=exercise_path,
        config=config,
        problem_md=problem_md,
    )


def discover_exercises(exercises_path: Path) -> list[Exercise]:
    """Discover all exercises in the exercises directory."""
    exercises_dir = exercises_path / "exercises"
    if not exercises_dir.exists():
        exercises_dir = exercises_path

    exercises: list[Exercise] = []

    for entry in sorted(exercises_dir.iterdir()):
        if entry.is_dir() and not entry.name.startswith((".", "_")):
            if (entry / "exercise.toml").exists() or (entry / "src").exists():
                exercises.append(load_exercise(entry))

    exercises.sort(key=lambda e: e.order)
    return exercises


def detect_language(exercise: Exercise, course_config: CourseConfig) -> str:
    """Detect the language for an exercise."""
    if exercise.config.test_command:
        cmd = exercise.config.test_command.lower()
        if "pytest" in cmd:
            if _has_torch_imports(exercise.src_path):
                return "pytorch"
            return "python"
        elif "vitest" in cmd or "jest" in cmd:
            if _has_react_imports(exercise.src_path) or course_config.language == "react":
                return "react"
            return "typescript" if _has_ts_files(exercise.src_path) else "javascript"
        elif "playwright" in cmd:
            return "html_css"

    if course_config.language in ("react", "pytorch"):
        return course_config.language

    src_path = exercise.src_path
    if src_path.exists():
        extensions = {f.suffix for f in src_path.rglob("*") if f.is_file()}
        if ".jsx" in extensions or (".tsx" in extensions and _has_react_imports(src_path)):
            return "react"
        elif ".ts" in extensions or ".tsx" in extensions:
            return "typescript"
        elif ".js" in extensions:
            if _has_react_imports(src_path):
                return "react"
            return "javascript"
        elif ".html" in extensions or ".css" in extensions:
            return "html_css"
        elif ".py" in extensions:
            if _has_torch_imports(src_path):
                return "pytorch"
            return "python"

    return course_config.language


def _has_torch_imports(src_path: Path) -> bool:
    """Check if any Python files import torch."""
    if not src_path.exists():
        return False
    for py_file in src_path.rglob("*.py"):
        try:
            content = py_file.read_text()
            if "import torch" in content or "from torch" in content:
                return True
        except Exception:
            pass
    return False


def _has_ts_files(src_path: Path) -> bool:
    """Check if directory contains TypeScript files."""
    if not src_path.exists():
        return False
    return any(src_path.rglob("*.ts")) or any(src_path.rglob("*.tsx"))


def _has_react_imports(src_path: Path) -> bool:
    """Check if any JS/TS files import React."""
    if not src_path.exists():
        return False
    for ext in ("*.js", "*.jsx", "*.ts", "*.tsx"):
        for js_file in src_path.rglob(ext):
            try:
                content = js_file.read_text()
                if "from 'react'" in content or 'from "react"' in content:
                    return True
                if "import React" in content:
                    return True
            except Exception:
                pass
    return False
