"""Abstract base adapter for test runners."""

from abc import ABC, abstractmethod

from exrun.models import Exercise, TestResult


class TestAdapter(ABC):
    """Abstract base class for language-specific test adapters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this adapter."""
        ...

    @abstractmethod
    def run_tests(self, exercise: Exercise, timeout: int = 30) -> TestResult:
        """Run tests for an exercise and return structured results."""
        ...

    @abstractmethod
    def get_default_command(self, exercise: Exercise) -> str:
        """Get the default test command for this adapter."""
        ...

    def is_available(self) -> bool:
        """Check if this adapter's dependencies are available."""
        return True
