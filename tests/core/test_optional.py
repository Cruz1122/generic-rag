import pytest
from generic_rag.core.optional import is_optional_dependency_available, require_optional_dependency
from generic_rag.core.exceptions import ConfigurationError

def test_is_available_for_core_deps():
    assert is_optional_dependency_available("pydantic") is True
    assert is_optional_dependency_available("httpx") is True

def test_is_available_for_missing_dep():
    assert is_optional_dependency_available("definitely_not_a_package_xyz_123") is False

def test_require_dependency_success():
    # pydantic should be available
    require_optional_dependency("pydantic", "core")

def test_require_dependency_failure():
    with pytest.raises(ConfigurationError) as excinfo:
        require_optional_dependency("definitely_missing_dep", "demo", "MyPackage")
    
    msg = str(excinfo.value)
    assert "Optional dependency 'MyPackage' is required" in msg
    assert 'pip install "generic-rag[demo]"' in msg

def test_require_dependency_failure_no_pkg_name():
    with pytest.raises(ConfigurationError) as excinfo:
        require_optional_dependency("definitely_missing_dep", "demo")
    
    msg = str(excinfo.value)
    assert "Optional dependency 'definitely_missing_dep' is required" in msg
