import pytest
from generic_rag.llm.dispatcher import DefaultLLMDispatcher
from generic_rag.core.schemas import LLMRequest, LLMResponse, ChatMessage, ProviderInfo
from generic_rag.core.exceptions import ConfigurationError

class MockProvider:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    async def generate(self, request):
        return LLMResponse(
            text=f"Hello from {self.name}",
            provider_info=ProviderInfo(name=self.name, model=request.model)
        )
    
    async def stream(self, request):
        pass

@pytest.mark.asyncio
async def test_dispatcher_resolves_default_provider():
    dispatcher = DefaultLLMDispatcher()
    provider1 = MockProvider("provider1")
    dispatcher.register_provider(provider1)
    
    req = LLMRequest(model="test", messages=[ChatMessage(role="user", content="hi")])
    res = await dispatcher.dispatch(req)
    assert res.text == "Hello from provider1"
    assert res.provider_info.name == "provider1"

@pytest.mark.asyncio
async def test_dispatcher_resolves_specific_provider():
    dispatcher = DefaultLLMDispatcher(default_provider_name="provider1")
    dispatcher.register_provider(MockProvider("provider1"))
    dispatcher.register_provider(MockProvider("provider2"))
    
    req = LLMRequest(provider="provider2", model="test", messages=[ChatMessage(role="user", content="hi")])
    res = await dispatcher.dispatch(req)
    assert res.text == "Hello from provider2"

@pytest.mark.asyncio
async def test_dispatcher_raises_configuration_error_missing_provider():
    dispatcher = DefaultLLMDispatcher()
    req = LLMRequest(model="test", messages=[ChatMessage(role="user", content="hi")])
    with pytest.raises(ConfigurationError, match="No provider specified"):
        await dispatcher.dispatch(req)

@pytest.mark.asyncio
async def test_dispatcher_raises_configuration_error_unregistered_provider():
    dispatcher = DefaultLLMDispatcher(default_provider_name="provider1")
    req = LLMRequest(model="test", messages=[ChatMessage(role="user", content="hi")])
    with pytest.raises(ConfigurationError, match="Provider 'provider1' is not registered"):
        await dispatcher.dispatch(req)
