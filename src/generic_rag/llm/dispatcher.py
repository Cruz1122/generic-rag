from typing import Dict, Optional
from generic_rag.core.schemas import LLMRequest, LLMResponse
from generic_rag.core.exceptions import ConfigurationError
from generic_rag.llm.base import BaseLLMDispatcher, BaseLLMProvider

class DefaultLLMDispatcher(BaseLLMDispatcher):
    def __init__(self, default_provider_name: Optional[str] = None):
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._default_provider_name = default_provider_name

    def register_provider(self, provider: BaseLLMProvider) -> None:
        self._providers[provider.name] = provider
        # Set first provider as default if none specified
        if not self._default_provider_name:
            self._default_provider_name = provider.name

    def get_provider(self, name: Optional[str]) -> BaseLLMProvider:
        provider_name = name or self._default_provider_name
        if not provider_name:
            raise ConfigurationError("No provider specified and no default provider set")
        
        provider = self._providers.get(provider_name)
        if not provider:
            raise ConfigurationError(f"Provider '{provider_name}' is not registered")
        
        return provider

    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        provider = self.get_provider(request.provider)
        return await provider.generate(request)
