"""Data models for exercise runner."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ExerciseStatus(Enum):
    PENDING = "pending"
    PASSED = "passed"
    SKIPPED = "skipped"


class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    HTML_CSS = "html_css"
    PYTORCH = "pytorch"
    REACT = "react"


@dataclass
class TestFailure:
    test_name: str
    message: str
    location: str | None = None


@dataclass
class TestResult:
    passed: bool
    tests_run: int
    tests_passed: int
    failures: list[TestFailure]
    output: str
    duration_ms: int = 0


@dataclass
class ExerciseConfig:
    name: str
    order: int
    difficulty: str = "beginner"
    test_command: str | None = None
    timeout_seconds: int = 30
    hints: list[str] = field(default_factory=list)
    hints_enabled: bool = True


@dataclass
class Exercise:
    path: Path
    config: ExerciseConfig
    problem_md: str = ""

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def order(self) -> int:
        return self.config.order

    @property
    def src_path(self) -> Path:
        return self.path / "src"

    @property
    def tests_path(self) -> Path:
        return self.path / "tests"


@dataclass
class CourseConfig:
    name: str
    version: str = "1.0.0"
    language: str = "python"
    test_runner: str = "pytest"
    show_hints: bool = True
    max_attempts_before_hint: int = 3


@dataclass
class ProjectConfig:
    exercises_path: Path
    default_language: str = "python"
    default_test_runner: str = "pytest"
