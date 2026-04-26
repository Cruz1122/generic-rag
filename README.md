# generic-rag

Agnostic framework for RAG (Retrieval-Augmented Generation) and LLM orchestration.

## Propósito

`generic-rag` es una librería pura de interfaces, modelos Pydantic y contratos diseñada para construir pipelines RAG y consumir modelos de lenguaje (OpenAI, Gemini, Groq, Ollama, etc.) **sin acoplamiento** a reglas de negocio, lógica de dominio (como AALIE) ni frameworks web (como FastAPI). Resuelve el problema de tener lógica de LLM, prompts específicos y recuperación de vectores fuertemente acoplados, permitiendo reutilizar la infraestructura base en múltiples proyectos.

## Qué incluye actualmente (v0.1)

- Contratos Pydantic estrictos (v2) para LLMs, Embeddings, Documentos y Chunks.
- Interfaces abstractas base para Providers, Dispatchers, Retrievers, ContextBuilders y VectorStores.
- **LLM Providers**: Implementaciones asíncronas basadas en `httpx` para OpenAI-compatible (Groq, LMStudio, vLLM), Ollama y Gemini REST API.
- **Ingestion**: `TextDocumentLoader` y `MarkdownDocumentLoader` puros.
- **Chunking**: `CharacterChunker` con soporte de superposición (overlap).
- **Embeddings**: `DeterministicEmbeddingProvider` para pruebas determinísticas offline.
- **Storage**: `InMemoryVectorStore` con similitud coseno pura en Python.
- **Retrieval**: `SimpleRetriever` agnóstico.
- **Context**: `XMLContextBuilder` para ensamblar chunks en prompts, y helpers de citación.
- **Pipeline**: `DefaultQAPipeline` que orquesta la recuperación, inyección de contexto y despacho al LLM.

## Qué NO incluye todavía

- Implementaciones de VectorStores listos para producción (ChromaDB, FAISS, Qdrant).
- Loaders pesados (PyMuPDF, OCR).
- Embeddings reales (Sentence Transformers).
- Dependencias pesadas o SDKs inflados (LangChain, LlamaIndex, Google Generative AI SDK).
- Endpoints de API o interfaces web.

## Instalación local

```bash
# Clonar o copiar el repositorio
cd generic-rag

# Instalar en modo editable con dependencias de desarrollo
pip install -e .[dev]
```

## Ejemplo mínimo de uso

Puedes ejecutar la demo funcional que corre en memoria sin necesidad de red:

```bash
python examples/basic_qa_demo.py
```

*Nota: La demo usa `DeterministicEmbeddingProvider` que genera vectores pseudo-aleatorios basados en el hash del texto. **No es semántico** y solo sirve para tests y demos estructurales.*

## Arquitectura por capas

Ver [ARCHITECTURE.md](docs/ARCHITECTURE.md) para un detalle exhaustivo de la arquitectura, diagrama y responsabilidades.

## Cómo crear un provider real o integrar desde otro proyecto

Para integrar en un proyecto (como AALIE), debes construir un **Adaptador**. El adaptador importa `generic-rag`, provee sus propios `ProviderConfig` (ej. API keys de variables de entorno), y configura el pipeline inyectando sus propios system prompts.

```python
from generic_rag.config import ProviderConfig
from generic_rag.llm.providers.openai_compatible import OpenAICompatibleProvider
from generic_rag.llm.dispatcher import DefaultLLMDispatcher

config = ProviderConfig(
    name="groq",
    api_key="...", # Pydantic SecretStr
    base_url="https://api.groq.com/openai/v1",
    default_model="llama-3.3-70b-versatile"
)
provider = OpenAICompatibleProvider(config)

dispatcher = DefaultLLMDispatcher()
dispatcher.register_provider(provider)

# Luego inyectas este dispatcher en DefaultQAPipeline...
```

Para crear un nuevo `VectorStore`, implementa `BaseVectorStore` desde `generic_rag.storage.base` asegurando soportar `index_chunks`, `search` y `delete_chunks`.
