class GenericRagError(Exception):
    """Clase base estricta."""
    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.message = message

class ConfigurationError(GenericRagError):
    pass

class ProviderError(GenericRagError):
    def __init__(self, message: str, provider: str = "unknown", status_code: int = None):
        super().__init__(f"[{provider}] {message}", provider, status_code)
        self.provider = provider
        self.status_code = status_code

class ProviderAuthError(ProviderError):
    pass

class ProviderTimeoutError(ProviderError):
    pass

class ProviderRateLimitError(ProviderError):
    pass

class InvalidResponseError(GenericRagError):
    def __init__(self, message: str, provider: str = "unknown", raw_content: str = None):
        super().__init__(f"[{provider}] {message}", provider, raw_content)
        self.provider = provider
        self.raw_content = raw_content

class ContextLimitError(GenericRagError):
    pass

class StorageError(GenericRagError):
    """Errores de base de datos vectorial o documental."""
    pass

class RetrievalError(GenericRagError):
    pass

class EmbeddingError(GenericRagError):
    pass

class DocumentLoadError(GenericRagError):
    pass

