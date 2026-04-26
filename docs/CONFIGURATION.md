# Configuración de Proveedores LLM

`generic-rag` permite configurar múltiples proveedores de modelos de lenguaje (LLMs) de forma segura y consistente. A continuación se muestran ejemplos de cómo configurarlos usando variables de entorno recomendadas y Pydantic.

## Advertencia de Testing

**Nota Importante:** Los tests en este repositorio **no hacen llamadas reales** a los proveedores. Todos los clientes HTTP y respuestas están mockeados para asegurar que la suite sea rápida, determinista y no incurra en costos ni dependa de conectividad. Para probar llamadas reales, por favor usa los scripts en el directorio `examples/`.

## Variables de Entorno Recomendadas

Aunque `generic-rag` no lee directamente las variables de entorno para imponer un comportamiento (tú pasas la configuración explícitamente), la convención recomendada para tus aplicaciones que lo consuman es:

- `GENERIC_RAG_PROVIDER`: Nombre del proveedor (ej. `ollama`, `openai-compatible`, `gemini`).
- `GENERIC_RAG_BASE_URL`: URL base del API.
- `GENERIC_RAG_API_KEY`: Clave de acceso al API.
- `GENERIC_RAG_MODEL`: Modelo por defecto a usar.

## Ejemplo: Ollama (Local)

Ollama es perfecto para desarrollo local sin costo.

```python
import os
from generic_rag.config import ProviderConfig
from generic_rag.llm.providers.ollama import OllamaProvider

config = ProviderConfig(
    name="ollama-local",
    base_url=os.getenv("GENERIC_RAG_BASE_URL", "http://localhost:11434"),
    default_model=os.getenv("GENERIC_RAG_MODEL", "llama3"),
    max_retries=2
)
provider = OllamaProvider(config)
```

## Ejemplo: OpenAI-Compatible (OpenAI, Groq, LM Studio)

Cualquier API que siga el estándar de OpenAI puede usar este proveedor.

```python
import os
from pydantic import SecretStr
from generic_rag.config import ProviderConfig
from generic_rag.llm.providers.openai_compatible import OpenAICompatibleProvider

api_key = os.getenv("GENERIC_RAG_API_KEY")

config = ProviderConfig(
    name="openai",
    base_url=os.getenv("GENERIC_RAG_BASE_URL", "https://api.openai.com/v1"),
    default_model=os.getenv("GENERIC_RAG_MODEL", "gpt-4o"),
    api_key=SecretStr(api_key) if api_key else None,
    max_retries=3,
    retry_backoff_seconds=2.0
)
provider = OpenAICompatibleProvider(config)
```

## Ejemplo: Google Gemini

```python
import os
from pydantic import SecretStr
from generic_rag.config import ProviderConfig
from generic_rag.llm.providers.gemini import GeminiProvider

api_key = os.getenv("GENERIC_RAG_API_KEY")

config = ProviderConfig(
    name="gemini",
    default_model=os.getenv("GENERIC_RAG_MODEL", "gemini-1.5-flash"),
    api_key=SecretStr(api_key) if api_key else None,
    max_retries=3
)
provider = GeminiProvider(config)
```

## Limitaciones Conocidas de Structured Output

El soporte para `json_schema` y `response_format="json_object"` varía por proveedor:

- **OpenAI-Compatible**: 
  - Soporta `json_schema` mapeando directamente al payload oficial (`response_format: {"type": "json_schema", ...}`).
  - Soporta `json_object` estándar.
  - Depende del servidor subyacente (vLLM, LM Studio, Groq, OpenAI) soportar estas llaves.
- **Ollama**:
  - Mapea el `json_schema` a la llave `format` en la petición.
  - Si se pide `json_object` sin schema, envía `format: "json"`.
  - Algunos modelos más pequeños de Ollama pueden no respetar estrictamente esquemas complejos.
- **Gemini**:
  - Soporta `json_schema` vía `responseSchema` en `generationConfig`.
  - Mapea `response_format="json_object"` a `responseMimeType="application/json"`.
