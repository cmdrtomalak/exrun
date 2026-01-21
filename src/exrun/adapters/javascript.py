"""JavaScript test adapter (Jest/Vitest)."""

from __future__ import annotations

import re
import shutil
import subprocess
import time
from pathlib import Path

from exrun.adapters.base import TestAdapter
from exrun.models import Exercise, TestFailure, TestResult


class JavaScriptAdapter(TestAdapter):
    """Adapter for JavaScript tests using Jest or Vitest."""

    @property
    def name(self) -> str:
        return "JavaScript (vitest/jest)"

    def _find_project_root(self, exercise: Exercise) -> Path:
        """Find the project root (where package.json lives)."""
        current = exercise.path
        while current.parent != current:
            if (current / "package.json").exists():
                return current
            current = current.parent
        return exercise.path

    def get_default_command(self, exercise: Exercise) -> str:
        project_root = self._find_project_root(exercise)
        if self._has_vitest(project_root):
            test_path = exercise.tests_path.relative_to(project_root)
            return f"npx vitest run {test_path} --reporter=verbose"
        return "npx jest --verbose"

    def _has_vitest(self, project_root: Path) -> bool:
        """Check if vitest is configured."""
        package_json = project_root / "package.json"
        if package_json.exists():
            content = package_json.read_text()
            return "vitest" in content
        return False

    def _install_dependencies(self, project_root: Path) -> TestResult:
        """Install npm dependencies if needed."""
        package_json = project_root / "package.json"
        if not package_json.exists():
            return TestResult(
                passed=True,
                tests_run=0,
                tests_passed=0,
                failures=[],
                output="No package.json found",
            )

        try:
            result = subprocess.run(
                "npm install",
                shell=True,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                return TestResult(
                    passed=False,
                    tests_run=0,
                    tests_passed=0,
                    failures=[TestFailure("npm_install", result.stderr[:500])],
                    output=result.stdout + result.stderr,
                )
            return TestResult(
                passed=True,
                tests_run=0,
                tests_passed=0,
                failures=[],
                output="Dependencies installed",
            )
        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                tests_run=0,
                tests_passed=0,
                failures=[TestFailure("npm_install", "npm install timed out")],
                output="npm install timed out after 120 seconds",
            )

    def run_tests(self, exercise: Exercise, timeout: int = 30) -> TestResult:
        project_root = self._find_project_root(exercise)

        if not (project_root / "node_modules").exists():
            install_result = self._install_dependencies(project_root)
            if not install_result.passed:
                return install_result

        cmd = self.get_default_command(exercise)

        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=project_root,
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
        """Parse Jest/Vitest output."""
        failures: list[TestFailure] = []

        pass_match = re.search(r"(\d+)\s+pass", output, re.IGNORECASE)
        fail_match = re.search(r"(\d+)\s+fail", output, re.IGNORECASE)

        tests_passed = int(pass_match.group(1)) if pass_match else 0
        tests_failed = int(fail_match.group(1)) if fail_match else 0

        failure_pattern = re.compile(r"[✕×]\s+(.+?)(?:\s+\(\d+.*?\))?$", re.MULTILINE)
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
        """Check if npm/node is available."""
        return shutil.which("npm") is not None
