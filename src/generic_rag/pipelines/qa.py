from abc import ABC, abstractmethod
from generic_rag.core.schemas import PipelineRequest, PipelineResponse

class BaseQAPipeline(ABC):
    @abstractmethod
    async def run(self, request: PipelineRequest) -> PipelineResponse:
        """
        Orquesta:
        1. retrieval.retrieve(request.retrieval)
        2. context.build_context(retrieved_chunks, request.context_options)
        3. inyectar contexto en request.llm.messages
        4. dispatcher.dispatch(request.llm)
        5. ensamblar PipelineResponse con citas.
        """
        pass
