"""Core orchestration logic."""

from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from exrun.adapters import get_adapter
from exrun.exercise import (
    detect_language,
    discover_exercises,
    find_config_file,
    load_course_config,
)
from exrun.models import CourseConfig, Exercise, ExerciseStatus, TestResult
from exrun.progress import ProgressDB


class ExerciseRunner:
    """Core exercise runner orchestration."""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()
        self._course_config: CourseConfig | None = None
        self._exercises: list[Exercise] = []
        self._progress_db: ProgressDB | None = None

    def initialize(self, exercises_path: Path | None = None) -> bool:
        """Initialize the runner by finding config and loading exercises."""
        if exercises_path:
            # Direct path provided - look for exrun.toml there
            config_path = exercises_path / "exrun.toml"
            if config_path.exists():
                self._course_config = load_course_config(config_path)
            else:
                # Create a default config for the path
                self._course_config = CourseConfig(
                    name="Unnamed Course",
                    exercises_path=exercises_path.resolve(),
                )
        else:
            config_path = find_config_file()
            if config_path:
                self._course_config = load_course_config(config_path)
            else:
                cwd = Path.cwd()
                # Check for exrun.toml or exercises directory
                if (cwd / "exrun.toml").exists():
                    self._course_config = load_course_config(cwd / "exrun.toml")
                elif (cwd / "exercises").exists():
                    self._course_config = CourseConfig(
                        name="Unnamed Course",
                        exercises_path=cwd / "exercises",
                    )
                else:
                    self.console.print(
                        "[red]No exrun.toml found and current directory is not an exercise course.[/red]"
                    )
                    return False

        exercises_path = self._course_config.exercises_path
        if not exercises_path.exists():
            self.console.print(f"[red]Exercises path not found: {exercises_path}[/red]")
            return False

        self._exercises = discover_exercises(exercises_path, self._course_config)

        if not self._exercises:
            self.console.print("[red]No exercises found.[/red]")
            return False

        db_path = exercises_path.parent / "progress.db"
        self._progress_db = ProgressDB(db_path)

        for ex in self._exercises:
            self._progress_db.ensure_exercise(ex)

        return True

    @property
    def exercises(self) -> list[Exercise]:
        return self._exercises

    @property
    def course_config(self) -> CourseConfig:
        if self._course_config is None:
            raise RuntimeError("Runner not initialized")
        return self._course_config

    @property
    def progress_db(self) -> ProgressDB:
        if self._progress_db is None:
            raise RuntimeError("Runner not initialized")
        return self._progress_db

    def get_current_exercise(self) -> Exercise | None:
        """Get the first non-passed exercise."""
        for exercise in self._exercises:
            status = self.progress_db.get_status(exercise)
            if status == ExerciseStatus.PENDING:
                return exercise
        return None

    def get_exercise_by_name(self, name: str) -> Exercise | None:
        """Find an exercise by name or order prefix."""
        for exercise in self._exercises:
            if exercise.name == name or exercise.path.name == name:
                return exercise
            # Check for order match (e.g., "1" or "1.2")
            if name == exercise.order_str:
                return exercise
        return None

    def run_exercise(self, exercise: Exercise) -> TestResult:
        """Run tests for a single exercise."""
        language = detect_language(exercise, self._course_config)
        adapter = get_adapter(language)

        self.console.print(f"\n[bold]Running tests for: {exercise.name}[/bold]")
        self.console.print(f"[dim]Using {adapter.name}[/dim]\n")

        result = adapter.run_tests(exercise, exercise.config.timeout_seconds)
        self.progress_db.record_attempt(exercise, result)

        return result

    def display_result(self, exercise: Exercise, result: TestResult) -> None:
        """Display test result with formatting."""
        if result.passed:
            self.console.print(
                Panel(
                    f"[green bold]✓ All {result.tests_passed} tests passed![/green bold]",
                    title=f"[green]{exercise.name}[/green]",
                    border_style="green",
                )
            )
        else:
            self.console.print(
                Panel(
                    f"[red bold]✗ {len(result.failures)} test(s) failed[/red bold]",
                    title=f"[red]{exercise.name}[/red]",
                    border_style="red",
                )
            )

            if result.failures:
                for failure in result.failures[:5]:
                    self.console.print(f"  [red]✗[/red] {failure.test_name}")
                    if failure.message:
                        msg = failure.message[:200]
                        self.console.print(f"    [dim]{msg}[/dim]")

    def display_problem(self, exercise: Exercise) -> None:
        """Display the problem description."""
        self.console.print(f"\n[bold cyan]Exercise: {exercise.name}[/bold cyan]\n")

        if exercise.problem_md:
            self.console.print(Markdown(exercise.problem_md))
        else:
            self.console.print("[dim]No problem description available.[/dim]")

        self.console.print(f"\n[dim]Edit files in: {exercise.src_path}[/dim]\n")

    def display_status(self) -> None:
        """Display current progress status."""
        table = Table(title="Exercise Progress")
        table.add_column("Order", style="dim")
        table.add_column("Exercise")
        table.add_column("Status")
        table.add_column("Attempts", justify="right")

        for exercise in self._exercises:
            status = self.progress_db.get_status(exercise)
            attempts = self.progress_db.get_attempts(exercise)

            if status == ExerciseStatus.PASSED:
                status_str = "[green]✓ Passed[/green]"
            elif status == ExerciseStatus.SKIPPED:
                status_str = "[yellow]⊘ Skipped[/yellow]"
            else:
                status_str = "[dim]○ Pending[/dim]"

            table.add_row(
                exercise.order_str,
                exercise.name,
                status_str,
                str(attempts) if attempts > 0 else "-",
            )

        self.console.print(table)

        current = self.get_current_exercise()
        if current:
            self.console.print(f"\n[bold]Current exercise:[/bold] {current.name}")
        else:
            self.console.print("\n[green bold]🎉 All exercises completed![/green bold]")

    def reset(self, exercise_name: str | None = None) -> None:
        """Reset progress for one or all exercises."""
        if exercise_name:
            exercise = self.get_exercise_by_name(exercise_name)
            if exercise:
                self.progress_db.reset_exercise(exercise)
                self.console.print(f"[green]Reset progress for: {exercise.name}[/green]")
            else:
                self.console.print(f"[red]Exercise not found: {exercise_name}[/red]")
        else:
            self.progress_db.reset_all()
            self.console.print("[green]All progress reset.[/green]")

    def skip_current(self) -> Exercise | None:
        """Skip the current exercise."""
        current = self.get_current_exercise()
        if current:
            self.progress_db.mark_skipped(current)
            self.console.print(f"[yellow]Skipped: {current.name}[/yellow]")
            return self.get_current_exercise()
        return None

    def verify_all(self) -> bool:
        """Verify all exercises pass (for course authors)."""
        all_passed = True

        for exercise in self._exercises:
            result = self.run_exercise(exercise)
            if result.passed:
                self.console.print(f"[green]✓[/green] {exercise.name}")
            else:
                self.console.print(f"[red]✗[/red] {exercise.name}")
                all_passed = False

        return all_passed

    def recheck_completed(self) -> list[tuple[Exercise, TestResult]]:
        """Re-run all previously passed exercises."""
        results: list[tuple[Exercise, TestResult]] = []

        for exercise in self._exercises:
            status = self.progress_db.get_status(exercise)
            if status == ExerciseStatus.PASSED:
                result = self.run_exercise(exercise)
                results.append((exercise, result))
                if not result.passed:
                    self.console.print(
                        f"[red]Regression: {exercise.name} no longer passes![/red]"
                    )

        return results

    def close(self) -> None:
        """Clean up resources."""
        if self._progress_db:
            self._progress_db.close()
