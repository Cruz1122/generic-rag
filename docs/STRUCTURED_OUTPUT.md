# Structured Output

`generic-rag` v0.2 provides unified support for requesting structured outputs (specifically JSON) from LLMs. This is crucial for data extraction tasks or when chaining LLM responses into strict system logic.

You control the output format using two fields on the `LLMRequest` model:
- `response_format`: `Literal["text", "json_object"]`
- `json_schema`: `Optional[Dict[str, Any]]`

## How to request JSON

### 1. Basic JSON Object Mode
If you only need the model to guarantee valid JSON syntax (but you handle the structure via system prompting), use `json_object`.

```python
request = LLMRequest(
    model="gpt-4o",
    messages=[
        ChatMessage(role="system", content="You are an assistant. Always output JSON."),
        ChatMessage(role="user", content="Extract the name: John is 30.")
    ],
    response_format="json_object"
)
```

### 2. Strict JSON Schema Mode
If you want the provider to enforce a specific schema (if supported by the underlying LLM), provide a valid JSON Schema dict.

```python
my_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}

request = LLMRequest(
    model="gpt-4o",
    messages=[
        ChatMessage(role="user", content="Extract the data: John is 30.")
    ],
    response_format="json_object",
    json_schema=my_schema
)
```

## Provider Support and Limitations

Different providers implement JSON structuring differently. `generic-rag` attempts to map your request to the provider's optimal capability, but you must be aware of the following limitations:

### OpenAI-Compatible
- **Schema Support**: Excellent. Maps directly to the official `{"type": "json_schema", "json_schema": {"schema": ...}}` payload.
- **Limitation**: Not all backends compatible with the OpenAI spec support the `json_schema` strict mode. For example, older versions of vLLM or specific models on Groq might reject the request if the schema is too complex or if strict Structured Outputs are not supported for that specific model.

### Ollama
- **Schema Support**: Good, but model-dependent. `generic-rag` maps the `json_schema` directly to the `format` key in the Ollama API payload.
- **Limitation**: If you request `json_object` without a schema, it sends `format: "json"`. Smaller models (like 7B or 8B parameters) might struggle to strictly follow deeply nested schemas even when passed to the `format` parameter.

### Gemini REST
- **Schema Support**: Good. Maps `response_format="json_object"` to `responseMimeType="application/json"` and maps the `json_schema` to `responseSchema` within the `generationConfig`.
- **Limitation**: Gemini has specific restrictions on what JSON Schema types it supports natively via the API. Ensure your schema is compatible with Google's API specification.

## Validating the Output

Currently, the `LLMResponse` object returns the raw string in `LLMResponse.text`. While the `structured` attribute exists on the Pydantic model (`LLMResponse.structured: Optional[Dict[str, Any]]`), the providers in v0.2 do not automatically run `json.loads(response.text)`. You are responsible for parsing the `response.text` string into a Python dictionary in your application layer.
