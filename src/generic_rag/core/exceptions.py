class GenericRagError(Exception):
    """Clase base estricta."""
    pass

class ConfigurationError(GenericRagError):
    pass

class ProviderError(GenericRagError):
    pass

class ProviderAuthError(ProviderError):
    pass

class ProviderTimeoutError(ProviderError):
    pass

class ProviderRateLimitError(ProviderError):
    pass

class InvalidResponseError(GenericRagError):
    pass

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
