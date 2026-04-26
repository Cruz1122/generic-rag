# Integration Adapters

`generic-rag` is designed to be an agnostic core library. This means it should not contain your application's business logic, web endpoints, or domain-specific prompts. Instead, you should build **Adapters** to connect your application to `generic-rag`.

## Why use Adapters?

- **Separation of Concerns**: Keep RAG orchestration separate from your web framework or domain logic.
- **Testability**: Test your application logic and your RAG pipelines independently.
- **Maintainability**: Easily switch web frameworks (e.g., from FastAPI to Flask) or LLM providers without rewriting your core logic.

## Recommended Patterns

### 1. Simple Domain Adapter
For small scripts or simple integrations, wrap the pipeline call in a function that handles domain-specific requests and responses.

See [examples/adapters/simple_domain_adapter.py](../examples/adapters/simple_domain_adapter.py).

### 2. Service Layer Pattern
For larger applications, create a service class that encapsulates the RAG pipeline. This service should use your application's Data Transfer Objects (DTOs).

See [examples/adapters/service_layer_adapter.py](../examples/adapters/service_layer_adapter.py).

### 3. Web Framework Integration (FastAPI)
Integrate `generic-rag` into your web API using dependency injection. Keep the API schemas separate from the library's internal schemas.

See [examples/adapters/fastapi_adapter_example.py](../examples/adapters/fastapi_adapter_example.py).

**Installation**:
To use the FastAPI example, install the optional extra:
```bash
pip install -e ".[fastapi]"
```

**Running the API**:
```bash
uvicorn examples.adapters.fastapi_adapter_example:app --reload
```

## Anti-Patterns to Avoid

- **Domain Prompts in Core**: Avoid adding prompts like "You are a legal assistant..." directly into the `generic-rag` library. Pass them via `PipelineRequest`.
- **Web Concerns in Core**: Never import `fastapi`, `flask`, or `httpx.Response` inside `src/generic_rag`.
- **Hardcoded Domain Logic**: Use the `metadata` fields in chunks and citations to store domain-specific info, rather than creating new fields in the library's schemas.
- **Real API calls in Tests**: Always use a fake/mock dispatcher (like `FakeLLMDispatcher` in the examples) for your application's unit tests.

## Summary of Examples

| Example | Pattern | Key Benefit |
|---------|---------|-------------|
| `simple_domain_adapter.py` | Functional Wrapper | Quick and easy integration |
| `service_layer_adapter.py` | Service Layer + DTOs | Clean architecture, high testability |
| `fastapi_adapter_example.py` | Dependency Injection | Industry standard for web APIs |
