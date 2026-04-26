import os

def provider_handler() -> int:
    env_vars = [
        "GENERIC_RAG_PROVIDER",
        "GENERIC_RAG_API_KEY",
        "GENERIC_RAG_BASE_URL",
        "GENERIC_RAG_MODEL",
        "GENERIC_RAG_EMBEDDINGS_BASE_URL",
        "GENERIC_RAG_EMBEDDINGS_API_KEY",
        "GENERIC_RAG_EMBEDDINGS_MODEL",
    ]

    for var in env_vars:
        value = os.environ.get(var)
        if value is None:
            print(f"{var}: missing")
        else:
            if any(secret in var for secret in ["KEY", "SECRET", "TOKEN"]):
                print(f"{var}: present (redacted)")
            elif "URL" in var:
                print(f"{var}: present")
            else:
                print(f"{var}: {value}")

    return 0
