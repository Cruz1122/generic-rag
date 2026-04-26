# Arquitectura de generic-rag

## Diagrama del Pipeline

```text
[PipelineRequest]
       │
       ▼
 1. [QAPipeline] ───────────► [Retriever]
       │                           │
       │                           ▼
       │                    [VectorStore] ◄─── (Embeddings & Chunks indexados previamente)
       │                           │
       │                           ▼
       │                    [ScoredChunks]
       ▼                           │
 2. [ContextBuilder] ◄─────────────┘
       │
       ▼
  (Genera XML Context String)
       │
       ▼
 3. Ensambla nuevo [LLMRequest] (inyectando contexto en mensajes)
       │
       ▼
 4. [LLMDispatcher]
       │
       ▼
 5. [LLMProvider] (OpenAI Compatible, Gemini, Ollama, etc.)
       │
       ▼
  [LLMResponse]
       │
       ▼
 6. Ensambla [PipelineResponse] (Respuesta + Chunks + Citas)
```

## Responsabilidades por Módulo

- **`core.schemas`**: Fuente de verdad absoluta. Define todos los modelos Pydantic v2 (Input/Output). Impide acoplamiento a dicts sueltos.
- **`ingestion`**: Transforma archivos físicos o bytes en `Document`s. El `Chunker` los divide en `Chunk`s preservando trazabilidad (`start_char`, `end_char`, `SourceRef`).
- **`embeddings`**: Interfaz pura para convertir texto en vectores densos.
- **`storage`**: Almacena y recupera `Chunk`s basados en similitud (ej. Coseno) e IDs. Totalmente separado de la estrategia de búsqueda.
- **`retrieval`**: Aplica estrategias (Híbridas, Densas, Umbrales) usando un `VectorStore` y un `EmbeddingProvider`.
- **`context`**: Transforma una lista de `ScoredChunk`s en un string seguro (ej. XML escapado) para inyectar en un LLM, respetando límites de tokens aproximados.
- **`llm`**: Despacha peticiones a proveedores unificados, normalizando errores HTTP (Timeouts, Auth, RateLimits) en excepciones propias.
- **`pipelines`**: Orquesta el flujo completo de pregunta/respuesta.

## Límites del Paquete

`generic-rag` **NO** debe conocer:
- Rutas HTTP (FastAPI, Flask, etc.).
- Lógica de UI o adaptadores de frontend.
- Prompts específicos de negocio ("Eres un asistente de algoritmos...").
- Estructuras de respuesta específicas de un dominio (ej. `QuizGenerationResponse`).
- Secretos harcodeados o variables de entorno directas (esto se inyecta vía `ProviderConfig`).

## Ejemplo de Integración Conceptual

Un proyecto consumidor (ej. "AALIE") debería tener una carpeta de adaptación:

```text
aalie/
  adapter/
    rag_setup.py    # Instancia QAPipeline, inyecta ChromaVectorStore y OpenAIProvider.
    prompts.py      # Define los system prompts gigantes de AALIE.
    services.py     # Llama a pipeline.run(...) pasándole los prompts y el schema de reparación.
```
