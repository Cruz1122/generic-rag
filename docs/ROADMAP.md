# Roadmap de generic-rag

### v0.1: Core Contracts & In-Memory Pipeline (Completado)
- Modelos Pydantic v2 y jerarquía de excepciones.
- Interfaces base para todo el ecosistema.
- Proveedores LLM asíncronos ligeros (OpenAI-compatible, Ollama, Gemini).
- Ingestión básica (TXT, MD) y chunking por caracteres.
- Almacenamiento en memoria con similitud coseno.
- Embedding determinístico para pruebas.
- QA Pipeline con Context Builder en XML.
- Extensiva suite de tests y ejemplos sin dependencias pesadas.

### v0.2: Providers Estables
- Soporte completo para streaming (`AsyncIterator[str]`) en todos los LLM providers.
- Manejo mejorado de retries con exponential backoff a nivel Dispatcher.

### v0.3: Loaders Opcionales (Extras)
- `generic-rag[pdf]`: PyMuPDFLoader.
- `generic-rag[html]`: BeautifulSoup HTML Loader.

### v0.4: Vector Stores Opcionales
- `generic-rag[chroma]`: Integración con ChromaDB.
- `generic-rag[qdrant]`: Integración con Qdrant.

### v0.5: Embeddings Reales Opcionales
- `generic-rag[embeddings]`: Soporte para `sentence-transformers` locales y APIs de embeddings (OpenAI, Voyage).

### v0.6: Adapter Examples
- Más ejemplos de integración y Rerankers (CrossEncoders).
