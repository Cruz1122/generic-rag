from abc import ABC, abstractmethod
from typing import List
from generic_rag.core.schemas import (
    PipelineRequest, PipelineResponse, LLMRequest, ChatMessage, ScoredChunk
)
from generic_rag.retrieval.base import BaseRetriever
from generic_rag.context.builder import BaseContextBuilder
from generic_rag.llm.base import BaseLLMDispatcher
from generic_rag.context.citations import build_citations

class BaseQAPipeline(ABC):
    @abstractmethod
    async def run(self, request: PipelineRequest) -> PipelineResponse:
        pass

class DefaultQAPipeline(BaseQAPipeline):
    def __init__(
        self, 
        retriever: BaseRetriever, 
        context_builder: BaseContextBuilder, 
        dispatcher: BaseLLMDispatcher
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.dispatcher = dispatcher

    async def run(self, request: PipelineRequest) -> PipelineResponse:
        # 1. Retrieve chunks
        retrieval_response = await self.retriever.retrieve(request.retrieval)
        retrieved_chunks = retrieval_response.chunks

        # 2. Build context
        context_str = self.context_builder.build_context(
            chunks=retrieved_chunks,
            options=request.context_options
        )

        # 3. Create a new LLMRequest to avoid mutating the original
        messages = list(request.llm.messages)
        
        # 4. Inject context
        prompt = (
            "Use the following retrieved context to answer the user query.\n"
            "If the context is insufficient, say so.\n\n"
            f"Retrieved context:\n{context_str}\n\n"
            f"User query:\n{request.query}"
        )
        
        messages.append(ChatMessage(role="user", content=prompt))
        
        llm_req = LLMRequest(
            provider=request.llm.provider,
            model=request.llm.model,
            messages=messages,
            temperature=request.llm.temperature,
            max_tokens=request.llm.max_tokens,
            timeout_seconds=request.llm.timeout_seconds,
            response_format=request.llm.response_format,
            json_schema=request.llm.json_schema,
            stream=request.llm.stream,
            metadata=request.llm.metadata
        )

        # 5. Dispatch to LLM
        answer = await self.dispatcher.dispatch(llm_req)

        # 6. Build citations
        citations = build_citations(retrieved_chunks)

        # 7. Return response
        return PipelineResponse(
            answer=answer,
            retrieved_chunks=retrieved_chunks,
            citations=citations
        )
