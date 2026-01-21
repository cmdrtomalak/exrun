"""Python/pytest test adapter."""

import re
import subprocess
import time

from exrun.adapters.base import TestAdapter
from exrun.models import Exercise, TestFailure, TestResult


class PythonAdapter(TestAdapter):
    """Adapter for Python tests using pytest."""

    @property
    def name(self) -> str:
        return "Python (pytest)"

    def get_default_command(self, exercise: Exercise) -> str:
        # Check for tests/ subdirectory first
        if exercise.tests_path.exists():
            return f"pytest {exercise.tests_path} -v --tb=short"
        # Otherwise run pytest in the exercise directory (flat structure)
        return "pytest -v --tb=short"

    def run_tests(self, exercise: Exercise, timeout: int = 30) -> TestResult:
        cmd = self.get_default_command(exercise)

        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=exercise.path,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=self._get_env(exercise),
            )
            output = result.stdout + result.stderr
            duration_ms = int((time.time() - start) * 1000)

            return self._parse_output(output, result.returncode == 0, duration_ms)

        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                tests_run=0,
                tests_passed=0,
                failures=[TestFailure("timeout", f"Tests timed out after {timeout}s")],
                output=f"Tests timed out after {timeout} seconds",
                duration_ms=timeout * 1000,
            )
        except Exception as e:
            return TestResult(
                passed=False,
                tests_run=0,
                tests_passed=0,
                failures=[TestFailure("error", str(e))],
                output=str(e),
                duration_ms=int((time.time() - start) * 1000),
            )

    def _get_env(self, exercise: Exercise) -> dict[str, str]:
        """Get environment variables for running tests."""
        import os

        env = os.environ.copy()
        # Add src/ to PYTHONPATH if it exists, otherwise add the exercise dir
        if exercise.src_path.exists():
            pythonpath = str(exercise.src_path)
        else:
            pythonpath = str(exercise.path)
        if "PYTHONPATH" in env:
            pythonpath = f"{pythonpath}:{env['PYTHONPATH']}"
        env["PYTHONPATH"] = pythonpath
        return env

    def _parse_output(self, output: str, success: bool, duration_ms: int) -> TestResult:
        """Parse pytest output to extract test results."""
        failures: list[TestFailure] = []

        summary_match = re.search(
            r"(\d+) passed(?:, (\d+) failed)?|(\d+) failed(?:, (\d+) passed)?",
            output,
        )

        tests_passed = 0
        tests_failed = 0

        if summary_match:
            groups = summary_match.groups()
            if groups[0]:
                tests_passed = int(groups[0])
                tests_failed = int(groups[1]) if groups[1] else 0
            elif groups[2]:
                tests_failed = int(groups[2])
                tests_passed = int(groups[3]) if groups[3] else 0

        failure_pattern = re.compile(
            r"FAILED\s+(\S+?)(?:::(\w+))?\s*-\s*(.+?)(?=\n(?:FAILED|=|$))",
            re.DOTALL,
        )

        for match in failure_pattern.finditer(output):
            test_file = match.group(1)
            test_name = match.group(2) or "unknown"
            message = match.group(3).strip()
            failures.append(TestFailure(
                test_name=f"{test_file}::{test_name}",
                message=message[:500],
                location=test_file,
            ))

        if not success and not failures:
            error_match = re.search(r"((?:Error|Exception|AssertionError).*?)(?=\n\n|\Z)", output, re.DOTALL)
            if error_match:
                failures.append(TestFailure(
                    test_name="test",
                    message=error_match.group(1).strip()[:500],
                ))

        tests_run = tests_passed + tests_failed
        if tests_run == 0 and not success:
            tests_run = 1

        return TestResult(
            passed=success,
            tests_run=tests_run,
            tests_passed=tests_passed,
            failures=failures,
            output=output,
            duration_ms=duration_ms,
        )
