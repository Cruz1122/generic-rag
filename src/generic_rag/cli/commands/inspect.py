import asyncio
import sys
from pathlib import Path
from importlib.util import find_spec

from generic_rag.ingestion.loaders import TextDocumentLoader, MarkdownDocumentLoader

def inspect_handler(args) -> int:
    path = Path(args.path)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        return 1
    if not path.is_file():
        print(f"Error: Not a file: {path}", file=sys.stderr)
        return 1

    suffix = path.suffix.lower()
    loader = None

    if suffix == ".txt":
        loader = TextDocumentLoader()
    elif suffix in [".md", ".markdown"]:
        loader = MarkdownDocumentLoader()
    elif suffix == ".pdf":
        if find_spec("fitz"):
            from generic_rag.ingestion.pdf import PyMuPDFDocumentLoader
            loader = PyMuPDFDocumentLoader()
        else:
            print("Error: PDF extra not installed.", file=sys.stderr)
            print('Install with: pip install -e ".[pdf]"', file=sys.stderr)
            return 1
    elif suffix in [".html", ".htm"]:
        if find_spec("bs4"):
            from generic_rag.ingestion.html import HTMLDocumentLoader
            loader = HTMLDocumentLoader()
        else:
            print("Error: HTML extra not installed.", file=sys.stderr)
            print('Install with: pip install -e ".[html]"', file=sys.stderr)
            return 1
    else:
        print(f"Error: Unsupported file extension: {suffix}", file=sys.stderr)
        return 1

    try:
        documents = asyncio.run(loader.load(str(path)))
    except Exception as e:
        print(f"Error loading document: {e}", file=sys.stderr)
        return 2

    print(f"file: {path}")
    print(f"documents: {len(documents)}")
    
    for i, doc in enumerate(documents):
        print(f"document[{i}].source_type: {doc.source.source_type}")
        if doc.source.title:
            print(f"document[{i}].title: {doc.source.title}")
        if doc.source.page:
            print(f"document[{i}].page: {doc.source.page}")
        print(f"document[{i}].content_length: {len(doc.content)}")
        preview = doc.content[:100].replace("\n", " ")
        if len(doc.content) > 100:
            preview += "..."
        print(f"document[{i}].preview: {preview}")

    return 0
