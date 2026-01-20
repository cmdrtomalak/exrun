"""TypeScript test adapter (Vitest with tsc)."""

import subprocess

from exrun.adapters.javascript import JavaScriptAdapter
from exrun.models import Exercise, TestFailure, TestResult


class TypeScriptAdapter(JavaScriptAdapter):
    """Adapter for TypeScript tests using Vitest with type checking."""

    @property
    def name(self) -> str:
        return "TypeScript (vitest)"

    def run_tests(self, exercise: Exercise, timeout: int = 30) -> TestResult:
        project_root = self._find_project_root(exercise)

        if not (project_root / "node_modules").exists():
            install_result = self._install_dependencies(project_root)
            if not install_result.passed:
                return install_result

        tsc_result = self._run_type_check(exercise)
        if not tsc_result.passed:
            return tsc_result

        return super().run_tests(exercise, timeout)

    def _run_type_check(self, exercise: Exercise) -> TestResult:
        """Run TypeScript type checking."""
        project_root = self._find_project_root(exercise)
        tsconfig = project_root / "tsconfig.json"

        if not tsconfig.exists():
            tsconfig = exercise.path / "tsconfig.json"
            if not tsconfig.exists():
                return TestResult(
                    passed=True,
                    tests_run=0,
                    tests_passed=0,
                    failures=[],
                    output="No tsconfig.json found, skipping type check",
                )

        try:
            result = subprocess.run(
                "npx tsc --noEmit",
                shell=True,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                return TestResult(
                    passed=False,
                    tests_run=1,
                    tests_passed=0,
                    failures=[TestFailure(
                        test_name="type_check",
                        message=(result.stdout + result.stderr)[:500],
                    )],
                    output=result.stdout + result.stderr,
                )

            return TestResult(
                passed=True,
                tests_run=0,
                tests_passed=0,
                failures=[],
                output="Type check passed",
            )

        except Exception as e:
            return TestResult(
                passed=False,
                tests_run=1,
                tests_passed=0,
                failures=[TestFailure("type_check", str(e))],
                output=str(e),
            )
