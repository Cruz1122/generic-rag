# generic-rag

Agnostic framework for RAG (Retrieval-Augmented Generation) and LLM orchestration.

## Propósito

Proveer una librería pura de interfaces, modelos Pydantic y contratos para construir pipelines RAG y consumir modelos de lenguaje (OpenAI, Gemini, Groq, Ollama, etc.) sin acoplamiento a reglas de negocio ni frameworks de UI.

## Qué incluye esta versión inicial
- Contratos Pydantic estrictos (v2) para LLMs, Embeddings, Documentos y Chunks.
- Interfaces abstractas para Providers, Dispatchers, Retrievers y VectorStores.
- Trazabilidad y tipos para citas de contexto (`Citation`, `SourceRef`).
- Jerarquía de excepciones (`GenericRagError`).
- Esqueleto agnóstico para `QAPipeline`.

## Qué NO incluye todavía
- Implementaciones concretas de proveedores (ej. `GeminiProvider`, `OpenAIProvider`).
- Implementaciones de VectorStores (ej. Chroma, FAISS).
- Implementaciones de carga y chunking (ej. PyMuPDF, Langchain chunkers).
- Endpoints de FastAPI o integraciones web.

## Ejemplo conceptual de uso

```python
from generic_rag.core.schemas import PipelineRequest, LLMRequest, RetrievalRequest
from generic_rag.pipelines.qa import BaseQAPipeline

# Esto se inyecta desde la implementación concreta
pipeline: BaseQAPipeline = mi_pipeline_configurado()

request = PipelineRequest(
    query="¿Cómo funciona el Attention Mechanism?",
    retrieval=RetrievalRequest(query="Attention Mechanism", top_k=5),
    llm=LLMRequest(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "¿Cómo funciona el Attention Mechanism?"}]
    )
)

response = await pipeline.run(request)
print(response.answer.text)
```

**Nota Importante:** Este paquete NO contiene reglas de negocio de ningún producto, ni directrices de "system prompts" específicas de algoritmos, pseudocódigo, u otras lógicas. Es una base de orquestación.
