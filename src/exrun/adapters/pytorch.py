"""PyTorch test adapter with GPU detection."""


from exrun.adapters.python import PythonAdapter
from exrun.models import Exercise, TestResult


class PyTorchAdapter(PythonAdapter):
    """Adapter for PyTorch tests using pytest with GPU handling."""

    @property
    def name(self) -> str:
        return "PyTorch (pytest)"

    def _get_env(self, exercise: Exercise) -> dict[str, str]:
        """Get environment variables, including CUDA settings."""
        env = super()._get_env(exercise)

        if not self._cuda_available():
            env["CUDA_VISIBLE_DEVICES"] = ""

        return env

    def _cuda_available(self) -> bool:
        """Check if CUDA is available."""
        try:
            import subprocess

            result = subprocess.run(
                ["python", "-c", "import torch; print(torch.cuda.is_available())"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip().lower() == "true"
        except Exception:
            return False

    def run_tests(self, exercise: Exercise, timeout: int = 30) -> TestResult:
        timeout = max(timeout, exercise.config.timeout_seconds, 60)
        return super().run_tests(exercise, timeout)

    def is_available(self) -> bool:
        """Check if PyTorch is installed."""
        try:
            import subprocess

            result = subprocess.run(
                ["python", "-c", "import torch"],
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False
