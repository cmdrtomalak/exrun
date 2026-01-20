"""File system watcher for watch mode."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable

from rich.console import Console
from watchfiles import Change, watch

if TYPE_CHECKING:
    from exrun.runner import ExerciseRunner


class ExerciseWatcher:
    """Watch exercise files for changes and trigger test runs."""

    def __init__(
        self,
        console: Console | None = None,
        debounce_ms: int = 500,
    ):
        self.console = console or Console()
        self.debounce_ms = debounce_ms
        self._stop = False

    def watch(
        self,
        exercise_path: Path,
        on_change: Callable[[set[tuple[Change, str]]], None],
    ) -> None:
        """Watch for file changes and call the callback."""
        watch_path = exercise_path / "src"
        if not watch_path.exists():
            watch_path = exercise_path

        self.console.print(f"[dim]Watching {watch_path} for changes...[/dim]")
        self.console.print("[dim]Press Ctrl+C to stop.[/dim]\n")

        try:
            for changes in watch(
                watch_path,
                debounce=self.debounce_ms,
                recursive=True,
            ):
                if self._stop:
                    break

                relevant_changes = {
                    (change, path)
                    for change, path in changes
                    if self._is_relevant_file(path)
                }

                if relevant_changes:
                    on_change(relevant_changes)

        except KeyboardInterrupt:
            pass

    def _is_relevant_file(self, path: str) -> bool:
        """Check if a file change should trigger a test run."""
        p = Path(path)

        if p.name.startswith("."):
            return False
        if "__pycache__" in path or ".pyc" in path:
            return False
        if "node_modules" in path:
            return False

        relevant_extensions = {
            ".py", ".js", ".ts", ".tsx", ".jsx",
            ".html", ".css", ".json",
        }

        return p.suffix in relevant_extensions

    def stop(self) -> None:
        """Signal the watcher to stop."""
        self._stop = True


def run_watch_mode(
    runner: ExerciseRunner,
    keep_going: bool = False,
) -> None:
    """Run the exercise runner in watch mode."""
    console = runner.console
    watcher = ExerciseWatcher(console)

    current = runner.get_current_exercise()
    if not current:
        console.print("[green bold]🎉 All exercises completed![/green bold]")
        return

    runner.display_problem(current)

    def on_change(changes: set[tuple[Change, str]]) -> None:
        nonlocal current

        if not current:
            return

        changed_files = [Path(p).name for _, p in changes]
        console.print(f"\n[dim]Files changed: {', '.join(changed_files)}[/dim]")

        result = runner.run_exercise(current)
        runner.display_result(current, result)

        if result.passed:
            next_exercise = runner.get_current_exercise()

            if next_exercise and next_exercise != current:
                if keep_going:
                    current = next_exercise
                    console.print("\n[bold green]→ Moving to next exercise[/bold green]")
                    runner.display_problem(current)
                else:
                    console.print("\n[bold]Press Enter to continue to next exercise...[/bold]")
                    try:
                        input()
                        current = next_exercise
                        runner.display_problem(current)
                    except (EOFError, KeyboardInterrupt):
                        pass
            elif not next_exercise:
                console.print("\n[green bold]🎉 All exercises completed![/green bold]")
                watcher.stop()

    try:
        watcher.watch(current.path, on_change)
    except KeyboardInterrupt:
        console.print("\n[dim]Watch mode stopped.[/dim]")
