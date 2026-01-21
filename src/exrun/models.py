"""Data models for exercise runner."""

from dataclasses import dataclass
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
    order: tuple[int, ...]  # Hierarchical ordering, e.g., (1, 2) for exercises/01_*/02_*
    timeout_seconds: int = 30


@dataclass
class Exercise:
    path: Path
    config: ExerciseConfig
    problem_md: str = ""

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def order(self) -> tuple[int, ...]:
        return self.config.order

    @property
    def order_str(self) -> str:
        """String representation of order for display."""
        return ".".join(str(o) for o in self.config.order)

    @property
    def src_path(self) -> Path:
        return self.path / "src"

    @property
    def tests_path(self) -> Path:
        return self.path / "tests"


@dataclass
class CourseConfig:
    """Configuration from exrun.toml."""

    name: str
    exercises_path: Path
    version: str = "1.0.0"
    language: str = "python"
    test_runner: str = "pytest"
    timeout_seconds: int = 30
