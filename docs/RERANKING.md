# Reranking

El Reranking es una técnica utilizada en sistemas RAG para mejorar la precisión de los resultados recuperados. 

Típicamente se aplica en dos fases:
1. **Retrieval**: Se buscan los `top_k` documentos más relevantes usando búsqueda vectorial (Bi-Encoders) o tradicional (BM25). Es rápido pero puede perder matices semánticos.
2. **Reranking**: Se toman los resultados del retrieval y se reordenan usando un modelo más potente (Cross-Encoder) que analiza la relación directa entre la consulta y cada fragmento de texto.

## ¿Cuándo usar Reranking?

- Cuando la precisión de la búsqueda vectorial base no es suficiente.
- Cuando tienes recursos computacionales para añadir una pequeña latencia extra a cambio de mejores respuestas.
- Para reducir el "ruido" en el contexto enviado al LLM.

## Rerankers Disponibles

### DeterministicReranker

Un reranker que no requiere modelos ni conexión a internet. Ordena los resultados basándose en la coincidencia exacta de palabras clave (*keyword overlap*) entre la consulta y el contenido del fragmento.

Es ideal para:
- Pruebas unitarias.
- Demos rápidas.
- Entornos con recursos extremadamente limitados.

```python
from generic_rag.reranking import DeterministicReranker

reranker = DeterministicReranker()
reranked_chunks = await reranker.rerank(query="mi consulta", chunks=chunks, top_n=5)
```

### CrossEncoderReranker (Opcional)

Utiliza modelos de la librería `sentence-transformers`. Este reranker es semántico y mucho más preciso.

#### Instalación

Requiere la dependencia opcional `rerankers`:

```bash
pip install "generic-rag[rerankers]"
```
Note: If the extra is not installed, using the reranker will raise a `ConfigurationError`.

#### Uso

```python
from generic_rag.reranking.cross_encoder import CrossEncoderReranker

reranker = CrossEncoderReranker(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
reranked_chunks = await reranker.rerank(query="¿Cuál es la capital de Francia?", chunks=chunks)
```

## Integración con DefaultQAPipeline

Puedes inyectar cualquier reranker en el pipeline estándar:

```python
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.reranking import DeterministicReranker

pipeline = DefaultQAPipeline(
    retriever=retriever,
    context_builder=context_builder,
    dispatcher=dispatcher,
    reranker=DeterministicReranker() # Opcional
)

response = await pipeline.run(request)
```

## Semántica de Scores

Cuando se aplica un reranker:
1. `ScoredChunk.score`: Se actualiza con el score del reranker para mantener la consistencia en el ordenamiento.
2. `ScoredChunk.metadata["retrieval_score"]`: Conserva el score original devuelto por el retriever.
3. `ScoredChunk.metadata["rerank_score"]`: Contiene el score calculado por el reranker.
4. `ScoredChunk.metadata["reranker"]`: Identifica el nombre del componente de reranking utilizado.

## Limitaciones y Costes

- **Latencia**: Los Cross-Encoders son más lentos que los Bi-Encoders. Se recomienda aplicarlos solo sobre un número reducido de fragmentos (ej. top 10-50).
- **Recursos**: El uso de `CrossEncoderReranker` requiere memoria RAM (y opcionalmente GPU) para cargar los modelos.
- **Modelos**: Por defecto, `sentence-transformers` descargará los modelos de Hugging Face la primera vez que se utilicen.
