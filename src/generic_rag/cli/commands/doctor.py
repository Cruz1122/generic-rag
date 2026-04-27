import sys
from generic_rag.core.optional import is_optional_dependency_available

def doctor_handler() -> int:
    print("core: ok")
    print(f"python: ok ({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})")
    
    # Check dependencies
    dependencies = {
        "pydantic": "pydantic",
        "httpx": "httpx",
        "qdrant": "qdrant_client",
        "pdf": "fitz",
        "html": "bs4",
        "fastapi": "fastapi",
        "rerankers": "sentence_transformers",
    }

    for label, package in dependencies.items():
        # Note: we prioritize checking if it's already in sys.modules 
        # to support testing with mocks easily.
        if package in sys.modules or is_optional_dependency_available(package):
            print(f"{label}: ok")
        else:
            print(f"{label}: not installed")

    return 0
