# Providers Setup

`generic-rag` provides robust, asynchronous implementations for interacting with popular Large Language Models.

We recommend injecting configuration via environment variables at the application layer, parsing them, and passing them to the `ProviderConfig` Pydantic model.

## Ollama

Ollama allows you to run open-source models locally without API costs or rate limits.

### Configuration Variables

- `GENERIC_RAG_BASE_URL`: `http://localhost:11434`
- `GENERIC_RAG_MODEL`: Name of the downloaded model (e.g., `llama3`, `qwen3.5`, `mistral`).

### Setup Notes

1. You must have Ollama installed and running (`ollama serve`).
2. You must have pulled the model you intend to use before querying it:
   ```powershell
   ollama pull qwen3.5
   ```

### Running the Example

```powershell
$env:GENERIC_RAG_BASE_URL="http://localhost:11434"
$env:GENERIC_RAG_MODEL="qwen3.5"
python examples/ollama_chat.py
```

---

## OpenAI-Compatible

This provider interacts with any server that implements the OpenAI Chat Completions API standard. This includes:
- OpenAI (`api.openai.com`)
- Groq (`api.groq.com/openai/v1`)
- LM Studio (Local, usually `http://localhost:1234/v1`)
- vLLM

### Configuration Variables

- `GENERIC_RAG_BASE_URL`: The base URL of the API.
- `GENERIC_RAG_API_KEY`: Your secret API key.
- `GENERIC_RAG_MODEL`: The specific model ID (e.g., `gpt-4o`, `llama3-8b-8192`).

### Setup Notes

1. Ensure the URL includes `/v1` (for example: `http://localhost:1234/v1`).
2. The model name must match exactly what your server exposes.
3. For local servers like LM Studio, `GENERIC_RAG_API_KEY` is usually ignored, but setting it to a dummy value is recommended (`lm-studio`).
4. If your server rejects `response_format.type = "json_object"` (HTTP 400), use JSON Schema structured output instead (`json_schema`) or fallback to plain text mode.

### Running the Example (Groq)

```powershell
$env:GENERIC_RAG_BASE_URL="https://api.groq.com/openai/v1"
$env:GENERIC_RAG_API_KEY="gsk_your_groq_api_key_here"
$env:GENERIC_RAG_MODEL="llama3-8b-8192"
python examples/openai_compatible_chat.py
```

### Running the Example (LM Studio)

```powershell
$env:GENERIC_RAG_BASE_URL="http://localhost:1234/v1"
$env:GENERIC_RAG_API_KEY="lm-studio"
$env:GENERIC_RAG_MODEL="dolphin3.0-llama3.1-8b"
python examples/openai_compatible_chat.py
```

---

## Gemini REST

This provider uses the Google Gemini REST API directly via HTTPX, avoiding the need for the heavy Google Generative AI SDK.

### Configuration Variables

- `GENERIC_RAG_PROVIDER`: `gemini`
- `GENERIC_RAG_API_KEY`: Your Google AI Studio API Key.
- `GENERIC_RAG_MODEL`: The Gemini model ID (e.g., `gemini-1.5-flash`).

### Conceptual Setup

While there isn't a dedicated demo script for Gemini in `examples/` out of the box, setting it up in your own code is straightforward:

```python
import os
import asyncio
from pydantic import SecretStr
from generic_rag.config import ProviderConfig
from generic_rag.llm.providers.gemini import GeminiProvider
from generic_rag.core.schemas import LLMRequest, ChatMessage

async def test_gemini():
    config = ProviderConfig(
        name="gemini",
        default_model=os.getenv("GENERIC_RAG_MODEL", "gemini-1.5-flash"),
        api_key=SecretStr(os.getenv("GENERIC_RAG_API_KEY", "YOUR_KEY")),
        max_retries=3
    )
    provider = GeminiProvider(config)
    
    request = LLMRequest(
        model=config.default_model,
        messages=[ChatMessage(role="user", content="Hello, Gemini!")]
    )
    
    response = await provider.generate(request)
    print(response.text)

if __name__ == "__main__":
    asyncio.run(test_gemini())
```
