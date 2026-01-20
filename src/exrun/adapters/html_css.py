"""HTML/CSS test adapter using Playwright."""

import re
import shutil
import subprocess
import time

from exrun.adapters.base import TestAdapter
from exrun.models import Exercise, TestFailure, TestResult


class HtmlCssAdapter(TestAdapter):
    """Adapter for HTML/CSS tests using Playwright."""

    @property
    def name(self) -> str:
        return "HTML/CSS (Playwright)"

    def get_default_command(self, exercise: Exercise) -> str:
        return f"npx playwright test {exercise.tests_path} --reporter=list"

    def run_tests(self, exercise: Exercise, timeout: int = 30) -> TestResult:
        cmd = exercise.config.test_command or self.get_default_command(exercise)

        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=exercise.path,
                capture_output=True,
                text=True,
                timeout=timeout,
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

    def _parse_output(self, output: str, success: bool, duration_ms: int) -> TestResult:
        """Parse Playwright output."""
        failures: list[TestFailure] = []

        pass_match = re.search(r"(\d+)\s+passed", output)
        fail_match = re.search(r"(\d+)\s+failed", output)

        tests_passed = int(pass_match.group(1)) if pass_match else 0
        tests_failed = int(fail_match.group(1)) if fail_match else 0

        failure_pattern = re.compile(r"✘.*?›\s*(.+?)(?:\s*\(\d+.*?\))?$", re.MULTILINE)
        for match in failure_pattern.finditer(output):
            failures.append(TestFailure(
                test_name=match.group(1).strip(),
                message="Test failed",
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

    def is_available(self) -> bool:
        """Check if Playwright is available."""
        return shutil.which("npx") is not None
