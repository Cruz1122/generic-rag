import pytest
from examples.adapters.simple_domain_adapter import run_simple_adapter_demo

@pytest.mark.asyncio
async def test_simple_adapter_demo_runs_without_error():
    """
    Smoke test to ensure the simple adapter example runs end-to-end offline.
    """
    await run_simple_adapter_demo()
    # If it finishes without exception, it passes.
