# Troubleshooting

This guide covers common issues you might encounter while setting up or using `generic-rag` v0.2.

## Installation Issues

### `ModuleNotFoundError: No module named 'generic_rag'`
**Cause**: The package was not installed in your current environment, or you are using the wrong Python interpreter.
**Fix**: Ensure your virtual environment is activated, then run:
```powershell
python -m pip install -e ".[dev]"
```

### PowerShell script execution fails (Activate.ps1)
**Cause**: Windows PowerShell execution policies prevent running unsigned scripts by default.
**Fix**: Open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```

## Testing Issues

### `pytest` does not find any tests
**Cause**: You might be running `pytest` from the wrong directory.
**Fix**: Ensure you are in the root directory of the repository (`generic-rag/`). Run with verbosity to see what is being collected:
```powershell
python -m pytest -vv
```

## LLM Provider Issues

### `ProviderAuthError` (401/403)
**Cause**: The API key provided is invalid, missing, or unauthorized for the requested model.
**Fix**: Verify your environment variables. 
```powershell
# Check current variables
Get-ChildItem Env:GENERIC_RAG*

# Reset the variable
$env:GENERIC_RAG_API_KEY="your_actual_key"
```

### `ProviderRateLimitError` (429)
**Cause**: You are sending too many requests, or you have exhausted your quota/credits on the provider (e.g., Groq, OpenAI).
**Fix**: The `DefaultLLMDispatcher` will automatically retry these errors based on `ProviderConfig.max_retries`. If it still fails, wait a few minutes or upgrade your API tier.

### `ProviderTimeoutError` (408/504 or local timeout)
**Cause**: The API took too long to respond, or the `timeout_seconds` in `ProviderConfig` is too low for the requested `max_tokens`.
**Fix**: Increase `timeout_seconds` in your configuration (default is 30s).

### `InvalidResponseError` (Invalid JSON)
**Cause**: The API returned a response that is not valid JSON (e.g., an HTML error page like a 502 Bad Gateway proxy error), or the expected JSON structure was entirely missing.
**Fix**: The error message will contain a truncated version of the raw content. Inspect the raw content to diagnose the server-side issue.

## Ollama Specific Issues

### Connection Refused (WinError 10061)
**Cause**: The Ollama background service is not running on your machine.
**Fix**: Start Ollama. You can usually do this by running `ollama serve` in a separate terminal or launching the Ollama desktop app.

### Model not found / "pull model" error
**Cause**: You specified a model in `GENERIC_RAG_MODEL` that you haven't downloaded to your local machine.
**Fix**: Check available models and pull the required one:
```powershell
ollama list
ollama pull llama3
```
