"""CLI with Typer."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Optional

import typer
from rich.console import Console

from exrun.runner import ExerciseRunner

if TYPE_CHECKING:
    from exrun.models import Exercise

app = typer.Typer(
    name="exrun",
    help="Multi-language exercise runner with test gating",
    no_args_is_help=True,
)

console = Console()


def get_runner(exercises_path: Path | None = None) -> ExerciseRunner:
    """Create and initialize an exercise runner."""
    runner = ExerciseRunner(console)
    if not runner.initialize(exercises_path):
        raise typer.Exit(1)
    return runner


@app.command()
def watch(
    keep_going: Annotated[
        bool,
        typer.Option("--keep-going", "-k", help="Auto-advance without prompting"),
    ] = False,
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
) -> None:
    """Start watch mode - rerun tests on file changes."""
    from exrun.watcher import run_watch_mode

    runner = get_runner(exercises_path)
    try:
        run_watch_mode(runner, keep_going=keep_going)
    finally:
        runner.close()


@app.command()
def run(
    exercise: Annotated[
        Optional[str],
        typer.Argument(help="Exercise name or number to run"),
    ] = None,
    recheck: Annotated[
        bool,
        typer.Option("--recheck", help="Re-run all previously passed exercises"),
    ] = False,
    keep_going: Annotated[
        bool,
        typer.Option("--keep-going", "-k", help="Continue through all exercises"),
    ] = False,
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
) -> None:
    """Run tests for an exercise or re-check completed exercises."""
    runner = get_runner(exercises_path)

    try:
        if recheck:
            console.print("[bold]Re-checking previously passed exercises...[/bold]\n")
            results = runner.recheck_completed()

            all_passed = all(r.passed for _, r in results)
            if all_passed:
                console.print(f"\n[green]All {len(results)} exercises still pass![/green]")
            else:
                failed = sum(1 for _, r in results if not r.passed)
                console.print(f"\n[red]{failed} exercise(s) have regressed.[/red]")
                raise typer.Exit(1)

            if keep_going:
                current = runner.get_current_exercise()
                if current:
                    console.print(f"\n[bold]Continuing from: {current.name}[/bold]")
                    _run_exercises_sequentially(runner, current)
            return

        if exercise:
            ex = runner.get_exercise_by_name(exercise)
            if not ex:
                console.print(f"[red]Exercise not found: {exercise}[/red]")
                raise typer.Exit(1)
            result = runner.run_exercise(ex)
            runner.display_result(ex, result)
            if not result.passed:
                raise typer.Exit(1)
        else:
            current = runner.get_current_exercise()
            if not current:
                console.print("[green]All exercises completed![/green]")
                return

            if keep_going:
                _run_exercises_sequentially(runner, current)
            else:
                result = runner.run_exercise(current)
                runner.display_result(current, result)
                if not result.passed:
                    raise typer.Exit(1)

    finally:
        runner.close()


def _run_exercises_sequentially(runner: ExerciseRunner, start: Exercise) -> None:
    """Run exercises sequentially starting from a given exercise."""
    current: Exercise | None = start

    while current:
        runner.display_problem(current)
        result = runner.run_exercise(current)
        runner.display_result(current, result)

        if not result.passed:
            console.print("\n[yellow]Fix the failing tests to continue.[/yellow]")
            raise typer.Exit(1)

        current = runner.get_current_exercise()

    console.print("\n[green bold]🎉 All exercises completed![/green bold]")


@app.command()
def status(
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
) -> None:
    """Show current progress status."""
    runner = get_runner(exercises_path)
    try:
        runner.display_status()
    finally:
        runner.close()


@app.command()
def reset(
    exercise: Annotated[
        Optional[str],
        typer.Argument(help="Specific exercise to reset (or all if not specified)"),
    ] = None,
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Skip confirmation"),
    ] = False,
) -> None:
    """Reset progress for one or all exercises."""
    runner = get_runner(exercises_path)

    try:
        if not force:
            target = exercise or "all exercises"
            if not typer.confirm(f"Reset progress for {target}?"):
                raise typer.Abort()

        runner.reset(exercise)
    finally:
        runner.close()


@app.command()
def skip(
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
) -> None:
    """Skip the current exercise."""
    runner = get_runner(exercises_path)

    try:
        next_ex = runner.skip_current()
        if next_ex:
            console.print(f"[bold]Next exercise: {next_ex.name}[/bold]")
            runner.display_problem(next_ex)
        else:
            console.print("[green]All exercises completed![/green]")
    finally:
        runner.close()


@app.command(name="list")
def list_exercises(
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
) -> None:
    """List all exercises with their status."""
    runner = get_runner(exercises_path)
    try:
        runner.display_status()
    finally:
        runner.close()


@app.command()
def verify(
    all_exercises: Annotated[
        bool,
        typer.Option("--all", help="Verify all exercises pass"),
    ] = False,
    exercises_path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Path to exercises directory"),
    ] = None,
) -> None:
    """Verify exercises (for course authors)."""
    runner = get_runner(exercises_path)

    try:
        if all_exercises:
            console.print("[bold]Verifying all exercises...[/bold]\n")
            if runner.verify_all():
                console.print("\n[green]All exercises verified![/green]")
            else:
                console.print("\n[red]Some exercises failed verification.[/red]")
                raise typer.Exit(1)
        else:
            console.print("Use --all to verify all exercises.")
    finally:
        runner.close()


@app.command()
def init(
    name: Annotated[
        str,
        typer.Option("--name", "-n", help="Course name"),
    ] = "My Course",
    language: Annotated[
        str,
        typer.Option("--language", "-l", help="Primary language"),
    ] = "python",
    path: Annotated[
        Optional[Path],
        typer.Option("--path", "-p", help="Where to create the course"),
    ] = None,
) -> None:
    """Initialize a new exercise course."""

    course_path = path or Path.cwd()
    course_path.mkdir(parents=True, exist_ok=True)

    exercises_toml = course_path / "exercises.toml"
    if exercises_toml.exists():
        console.print(f"[yellow]exercises.toml already exists at {course_path}[/yellow]")
        raise typer.Exit(1)

    test_runner = {
        "python": "pytest",
        "pytorch": "pytest",
        "javascript": "vitest",
        "typescript": "vitest",
        "react": "vitest",
        "html_css": "playwright",
    }.get(language, "pytest")

    exercises_toml.write_text(f'''[course]
name = "{name}"
version = "1.0.0"
language = "{language}"
test_runner = "{test_runner}"

[settings]
show_hints = true
max_attempts_before_hint = 3
''')

    exercises_dir = course_path / "exercises"
    exercises_dir.mkdir(exist_ok=True)

    ex1_dir = exercises_dir / "01_hello"
    ex1_dir.mkdir(exist_ok=True)
    (ex1_dir / "src").mkdir(exist_ok=True)
    (ex1_dir / "tests").mkdir(exist_ok=True)

    (ex1_dir / "exercise.toml").write_text('''[exercise]
name = "Hello World"
order = 1
difficulty = "beginner"

[hints]
enabled = true
hints = [
    "Start by defining a simple function",
    "Return a string from the function"
]
''')

    (ex1_dir / "problem.md").write_text('''# Hello World

Welcome to your first exercise!

## Task

Create a function called `hello()` that returns the string `"Hello, World!"`.

## Example

```python
result = hello()
print(result)  # "Hello, World!"
```
''')

    if language in ("python", "pytorch"):
        (ex1_dir / "src" / "main.py").write_text('''# TODO: Implement the hello function

def hello():
    # Return "Hello, World!"
    pass
''')

        (ex1_dir / "tests" / "test_main.py").write_text('''from main import hello


def test_hello():
    assert hello() == "Hello, World!"
''')

    console.print(f"[green]Created new course at {course_path}[/green]")
    console.print("  - exercises.toml")
    console.print("  - exercises/01_hello/")
    console.print("\nRun [bold]exrun watch[/bold] to start!")


if __name__ == "__main__":
    app()
