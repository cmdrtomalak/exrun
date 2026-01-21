"""Exercise metadata parsing."""

import re
import tomllib
from pathlib import Path

from exrun.models import CourseConfig, Exercise, ExerciseConfig


def find_config_file(start_path: Path | None = None) -> Path | None:
    """Find exrun.toml by searching upward from start_path."""
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()
    home = Path.home()

    while current != current.parent:
        config_path = current / "exrun.toml"
        if config_path.exists():
            return config_path
        if current == home:
            break
        current = current.parent

    global_config = home / ".config" / "exrun" / "config.toml"
    if global_config.exists():
        return global_config

    return None


def load_course_config(config_path: Path) -> CourseConfig:
    """Load course configuration from exrun.toml.

    The exrun.toml only needs minimal configuration:
    - exercises_path: path to directory containing exercises

    Everything else is optional with sensible defaults.
    """
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    course = data.get("course", {})
    settings = data.get("settings", {})

    exercises_path_str = course.get("exercises_path", "./exercises")
    if exercises_path_str.startswith(("http://", "https://", "git@")):
        raise NotImplementedError("Remote exercise fetching not yet supported")

    exercises_path = Path(exercises_path_str)
    if not exercises_path.is_absolute():
        exercises_path = config_path.parent / exercises_path

    return CourseConfig(
        name=course.get("name", "Unnamed Course"),
        exercises_path=exercises_path.resolve(),
        version=course.get("version", "1.0.0"),
        language=course.get("language", "python"),
        test_runner=course.get("test_runner", "pytest"),
        timeout_seconds=settings.get("timeout_seconds", 30),
    )


def _extract_order_from_name(name: str) -> int:
    """Extract order number from exercise directory name.

    Supports patterns like:
    - '01_variables' -> 1
    - 'ex01_hello' -> 1
    - 'exercise_01_intro' -> 1

    Returns 999 if no numeric prefix found.
    """
    # Try numeric prefix first: 01_variables
    match = re.match(r"^(\d+)", name)
    if match:
        return int(match.group(1))

    # Try ex/exercise prefix: ex01_hello, exercise01_intro
    match = re.match(r"^(?:ex|exercise)[-_]?(\d+)", name, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try finding first number in the name
    match = re.search(r"(\d+)", name)
    if match:
        return int(match.group(1))

    return 999


def _get_hierarchical_order(exercise_path: Path, exercises_root: Path) -> tuple[int, ...]:
    """Get hierarchical order from path structure.

    For example:
    - exercises/01_basics/01_hello -> (1, 1)
    - exercises/01_basics/02_world -> (1, 2)
    - exercises/02_advanced/01_first -> (2, 1)
    """
    relative_path = exercise_path.relative_to(exercises_root)
    parts = relative_path.parts
    orders = tuple(_extract_order_from_name(part) for part in parts)
    return orders


def _format_exercise_name(dir_name: str) -> str:
    """Convert directory name like '01_hello_world' to 'Hello World'."""
    # Remove numeric prefix
    name = re.sub(r"^\d+_", "", dir_name)
    # Replace underscores with spaces and title case
    return name.replace("_", " ").title()


def load_exercise(
    exercise_path: Path,
    exercises_root: Path,
    course_config: CourseConfig,
) -> Exercise:
    """Load a complete exercise from its directory.

    Exercise metadata is derived from:
    - Directory name for order and display name
    - problem.md for description
    - Course defaults for timeout, language, etc.
    """
    # Get hierarchical order from directory structure
    order = _get_hierarchical_order(exercise_path, exercises_root)

    # Name from directory
    name = _format_exercise_name(exercise_path.name)

    # Build config from directory info and course defaults
    config = ExerciseConfig(
        name=name,
        order=order,
        timeout_seconds=course_config.timeout_seconds,
    )

    # Load problem description
    problem_path = exercise_path / "problem.md"
    problem_md = ""
    if problem_path.exists():
        problem_md = problem_path.read_text()

    return Exercise(
        path=exercise_path,
        config=config,
        problem_md=problem_md,
    )


def _is_exercise_dir(path: Path) -> bool:
    """Check if a directory is an exercise.

    An exercise directory is detected if it has:
    - src/ subdirectory, or
    - tests/ subdirectory, or
    - test_*.py files (for flat structure), or
    - solution.py file (for flat structure)
    """
    if not path.is_dir():
        return False

    # Check for standard structure
    if (path / "src").exists() or (path / "tests").exists():
        return True

    # Check for flat structure with test files
    if any(path.glob("test_*.py")):
        return True

    # Check for solution.py pattern
    if (path / "solution.py").exists():
        return True

    return False


def _discover_exercises_recursive(
    current_path: Path,
    exercises_root: Path,
    course_config: CourseConfig,
) -> list[Exercise]:
    """Recursively discover exercises, supporting nested directories."""
    exercises: list[Exercise] = []

    # Get entries sorted by their numeric prefix
    entries = sorted(
        current_path.iterdir(),
        key=lambda p: (_extract_order_from_name(p.name), p.name),
    )

    for entry in entries:
        if not entry.is_dir():
            continue
        if entry.name.startswith((".", "_")):
            continue
        if entry.name == "node_modules":
            continue

        if _is_exercise_dir(entry):
            # This is an exercise directory
            exercises.append(load_exercise(entry, exercises_root, course_config))
        else:
            # Check for nested exercises
            nested = _discover_exercises_recursive(entry, exercises_root, course_config)
            exercises.extend(nested)

    return exercises


def discover_exercises(exercises_path: Path, course_config: CourseConfig) -> list[Exercise]:
    """Discover all exercises in the exercises directory.

    Exercises are discovered recursively and ordered by their directory names.
    Directory names like '01_basics' and '02_advanced' determine order.
    """
    if not exercises_path.exists():
        return []

    exercises = _discover_exercises_recursive(exercises_path, exercises_path, course_config)

    # Sort by hierarchical order
    exercises.sort(key=lambda e: e.order)

    return exercises


def detect_language(exercise: Exercise, course_config: CourseConfig) -> str:
    """Detect the language for an exercise."""
    if course_config.language in ("react", "pytorch"):
        return course_config.language

    # Check src/ directory first, then exercise directory for flat structure
    src_path = exercise.src_path if exercise.src_path.exists() else exercise.path

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
