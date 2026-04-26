import pytest
from unittest.mock import AsyncMock
from generic_rag.core.schemas import LLMRequest, ChatMessage, LLMResponse, TokenUsage, ProviderInfo
from generic_rag.core.exceptions import ProviderTimeoutError, ProviderAuthError, ProviderRateLimitError
from generic_rag.llm.dispatcher import DefaultLLMDispatcher
from generic_rag.llm.base import BaseLLMProvider
from generic_rag.config import ProviderConfig

class MockProvider(BaseLLMProvider):
    def __init__(self, name: str, max_retries: int = 2):
        self._name = name
        self.config = ProviderConfig(name=name, default_model="test", max_retries=max_retries, retry_backoff_seconds=0.01)
        self.call_count = 0
        self.error_to_raise = None
        self.success_on_call = -1
    
    @property
    def name(self) -> str:
        return self._name
        
    async def generate(self, request: LLMRequest) -> LLMResponse:
        self.call_count += 1
        if self.call_count == self.success_on_call:
            return LLMResponse(
                text="Success", 
                usage=TokenUsage(), 
                provider_info=ProviderInfo(name=self.name, model=request.model)
            )
        if self.error_to_raise:
            raise self.error_to_raise
        return LLMResponse(
            text="Success", 
            usage=TokenUsage(), 
            provider_info=ProviderInfo(name=self.name, model=request.model)
        )
        
    async def stream(self, request):
        pass

@pytest.fixture
def request_obj():
    return LLMRequest(
        provider="mock",
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")]
    )

@pytest.mark.asyncio
async def test_dispatcher_retry_on_timeout(request_obj):
    provider = MockProvider("mock", max_retries=2)
    provider.error_to_raise = ProviderTimeoutError("Timeout")
    provider.success_on_call = 3 # Succeeds on 3rd try
    
    dispatcher = DefaultLLMDispatcher()
    dispatcher.register_provider(provider)
    
    res = await dispatcher.dispatch(request_obj)
    assert res.text == "Success"
    assert provider.call_count == 3

@pytest.mark.asyncio
async def test_dispatcher_no_retry_on_auth_error(request_obj):
    provider = MockProvider("mock", max_retries=2)
    provider.error_to_raise = ProviderAuthError("Auth")
    
    dispatcher = DefaultLLMDispatcher()
    dispatcher.register_provider(provider)
    
    with pytest.raises(ProviderAuthError):
        await dispatcher.dispatch(request_obj)
    
    assert provider.call_count == 1 # Only 1 call, no retries

@pytest.mark.asyncio
async def test_dispatcher_max_retries_exceeded(request_obj):
    provider = MockProvider("mock", max_retries=2)
    provider.error_to_raise = ProviderRateLimitError("Rate limit")
    
    dispatcher = DefaultLLMDispatcher()
    dispatcher.register_provider(provider)
    
    with pytest.raises(ProviderRateLimitError):
        await dispatcher.dispatch(request_obj)
    
    assert provider.call_count == 3 # 1 initial + 2 retries
