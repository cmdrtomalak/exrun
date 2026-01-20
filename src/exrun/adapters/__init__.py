"""Language-specific test adapters."""

from exrun.adapters.base import TestAdapter
from exrun.adapters.html_css import HtmlCssAdapter
from exrun.adapters.javascript import JavaScriptAdapter
from exrun.adapters.python import PythonAdapter
from exrun.adapters.pytorch import PyTorchAdapter
from exrun.adapters.react import ReactAdapter
from exrun.adapters.typescript import TypeScriptAdapter

__all__ = [
    "TestAdapter",
    "PythonAdapter",
    "JavaScriptAdapter",
    "TypeScriptAdapter",
    "HtmlCssAdapter",
    "PyTorchAdapter",
    "ReactAdapter",
    "get_adapter",
]


def get_adapter(language: str) -> TestAdapter:
    """Get the appropriate adapter for a language."""
    adapters: dict[str, type[TestAdapter]] = {
        "python": PythonAdapter,
        "javascript": JavaScriptAdapter,
        "typescript": TypeScriptAdapter,
        "html_css": HtmlCssAdapter,
        "pytorch": PyTorchAdapter,
        "react": ReactAdapter,
    }
    adapter_class = adapters.get(language, PythonAdapter)
    return adapter_class()
