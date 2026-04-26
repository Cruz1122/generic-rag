from abc import ABC, abstractmethod
from typing import AsyncIterator
from generic_rag.core.schemas import LLMRequest, LLMResponse

class BaseLLMProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        pass
        
    @abstractmethod
    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        pass

class BaseLLMDispatcher(ABC):
    @abstractmethod
    def register_provider(self, provider: BaseLLMProvider) -> None:
        pass
        
    @abstractmethod
    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        pass
