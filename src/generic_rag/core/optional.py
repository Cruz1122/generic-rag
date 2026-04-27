from importlib.util import find_spec
from generic_rag.core.exceptions import ConfigurationError

def is_optional_dependency_available(import_name: str) -> bool:
    """Check if an optional dependency is available without importing it."""
    try:
        return find_spec(import_name) is not None
    except (ImportError, ValueError):
        return False

def require_optional_dependency(import_name: str, extra_name: str, package_name: str | None = None) -> None:
    """
    Ensure an optional dependency is available.
    Raises ConfigurationError with a clear instruction if missing.
    """
    if not is_optional_dependency_available(import_name):
        pkg = package_name or import_name
        raise ConfigurationError(
            f"Optional dependency '{pkg}' is required for this feature. "
            f"Install it using: pip install \"generic-rag[{extra_name}]\""
        )
