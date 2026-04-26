import asyncio
import logging
from typing import Dict, Optional
from generic_rag.core.schemas import LLMRequest, LLMResponse
from generic_rag.core.exceptions import (
    ConfigurationError, ProviderError, ProviderTimeoutError, ProviderRateLimitError
)
from generic_rag.llm.base import BaseLLMDispatcher, BaseLLMProvider

logger = logging.getLogger(__name__)

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
        
        # Use duck typing to get config if available, fallback to defaults
        max_retries = getattr(provider, "config", None) and getattr(provider.config, "max_retries", 0) or 0
        backoff = getattr(provider, "config", None) and getattr(provider.config, "retry_backoff_seconds", 1.0) or 1.0

        for attempt in range(max_retries + 1):
            try:
                return await provider.generate(request)
            except (ProviderTimeoutError, ProviderRateLimitError) as e:
                if attempt == max_retries:
                    raise
                logger.warning(f"Transient error with {provider.name}: {e}. Retrying {attempt + 1}/{max_retries} in {backoff}s...")
            except ProviderError as e:
                if e.status_code and e.status_code >= 500:
                    if attempt == max_retries:
                        raise
                    logger.warning(f"Server error with {provider.name}: {e}. Retrying {attempt + 1}/{max_retries} in {backoff}s...")
                else:
                    raise
            
            await asyncio.sleep(backoff)

