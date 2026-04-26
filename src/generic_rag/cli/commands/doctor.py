import sys
from importlib.util import find_spec

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
        found = False
        try:
            # Check if it's already loaded (common in tests with mocks)
            if package in sys.modules:
                found = True
            else:
                found = find_spec(package) is not None
        except (ValueError, ImportError):
            found = False
            
        if found:
            print(f"{label}: ok")
        else:
            print(f"{label}: not installed")

    return 0
