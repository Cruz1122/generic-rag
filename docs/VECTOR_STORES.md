# Vector Stores

`generic-rag` soporta múltiples backends para el almacenamiento y recuperación de vectores.

## Backends Soportados

| Backend | Clase | Extra | Cuándo usarlo |
|---------|-------|-------|---------------|
| **In-Memory** | `InMemoryVectorStore` | Ninguno | Desarrollo local, pruebas, datasets pequeños (< 10k chunks). |
| **Qdrant** | `QdrantVectorStore` | `[qdrant]` | Producción, persistencia, datasets grandes, búsqueda asíncrona robusta. |

---

## InMemoryVectorStore

Es el backend por defecto. No requiere dependencias externas ni servicios corriendo. Los datos se pierden al cerrar el proceso.

```python
from generic_rag.storage import InMemoryVectorStore

store = InMemoryVectorStore()
```

---

## QdrantVectorStore

Primer vector store externo soportado. Utiliza el cliente oficial asíncrono de Qdrant.

### Instalación

```bash
pip install generic-rag[qdrant]
```

### Uso

```python
from qdrant_client import AsyncQdrantClient
from generic_rag.storage import QdrantVectorStore

client = AsyncQdrantClient("http://localhost:6333")

store = QdrantVectorStore(
    client=client,
    collection_name="my_collection",
    vector_size=1536, # Tamaño de tus embeddings
    distance="Cosine" # "Cosine", "Dot" o "Euclid"
)

# Es obligatorio asegurar que la colección existe antes de indexar
await store.ensure_collection(recreate=False)
```

### Características de la implementación v0.4

- **IDs Determinísticos**: Los IDs de Qdrant se generan mediante UUIDv5 basado en el `chunk_id`, garantizando que no haya duplicados si se re-indexa el mismo contenido.
- **Payload Completo**: Se guarda el `content` y todos los metadatos en Qdrant, permitiendo la reconstrucción completa del `ScoredChunk` sin necesidad de un DocumentStore externo.
- **Filtros Exactos**: Soporta filtrado simple por cualquier campo del payload (ej: `{"source.source_type": "pdf"}`).
- **Borrado Eficiente**: `delete_chunks(document_ids)` utiliza el selector `MatchAny` de Qdrant para borrar múltiples documentos en una sola llamada.

### Limitaciones Actuales

- No soporta búsqueda híbrida (sparse vectors).
- No soporta operadores lógicos complejos (OR, Rangos) en filtros.
- No gestiona índices de payload automáticamente.
- `recreate=True` en `ensure_collection` es una operación destructiva.
