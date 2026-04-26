import pytest
from pydantic import ValidationError, SecretStr
from generic_rag.config import ProviderConfig

def test_provider_config_valid():
    config = ProviderConfig(
        name="test",
        api_key=SecretStr("secret123"),
        base_url="http://test",
        default_model="gpt-4",
        timeout_seconds=60,
        max_retries=5,
        retry_backoff_seconds=1.5,
        extra_headers={"X-Test": "1"},
        extra_params={"temp": 0.5}
    )
    assert config.name == "test"
    assert config.api_key.get_secret_value() == "secret123"
    assert config.timeout_seconds == 60
    assert config.max_retries == 5
    assert config.retry_backoff_seconds == 1.5

def test_provider_config_secrets_not_exposed():
    config = ProviderConfig(
        name="test",
        api_key=SecretStr("supersecret"),
        default_model="test-model"
    )
    repr_str = repr(config)
    str_str = str(config)
    assert "supersecret" not in repr_str
    assert "supersecret" not in str_str
    assert "**********" in repr_str or "SecretStr" in repr_str

def test_provider_config_defaults():
    config = ProviderConfig(
        name="test",
        default_model="test-model"
    )
    assert config.timeout_seconds == 30
    assert config.max_retries == 3
    assert config.retry_backoff_seconds == 2.0
    assert config.api_key is None
    assert config.extra_headers == {}
    assert config.extra_params == {}
