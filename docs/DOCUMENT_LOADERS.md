# Document Loaders

`generic-rag` provides lightweight, framework-agnostic document loaders to ingest various file formats into standard `Document` objects.

## Core Loaders (Built-in)

These loaders are always available and have no external dependencies.

### `TextDocumentLoader`
Reads plain text files (`.txt`).
```python
from generic_rag.ingestion.loaders import TextDocumentLoader
loader = TextDocumentLoader()
docs = await loader.load("path/to/file.txt")
```

### `MarkdownDocumentLoader`
Reads Markdown files (`.md`).
```python
from generic_rag.ingestion.loaders import MarkdownDocumentLoader
loader = MarkdownDocumentLoader()
docs = await loader.load("path/to/file.md")
```

## Optional Loaders

To keep the core library small, advanced loaders require optional dependencies.

### `PyMuPDFDocumentLoader` (PDF)
Extracts text from PDF files using `PyMuPDF` (`fitz`).

**Installation:**
```bash
pip install "generic-rag[pdf]"
```
Note: If the extra is not installed, instantiating the loader will raise a `ConfigurationError`.

**Usage:**
```python
from generic_rag.ingestion.pdf import PyMuPDFDocumentLoader
loader = PyMuPDFDocumentLoader()
# Returns one Document per page
docs = await loader.load("path/to/document.pdf")
```

**Features & Limitations:**
- **Granularity:** Returns one `Document` per page, preserving page numbers in `SourceRef.page`.
- **No OCR:** It extracts embedded text. Scanned pages will return empty text.
- **Layouts:** Complex multi-column layouts might result in imperfect reading order.

### `HTMLDocumentLoader` (HTML)
Extracts and cleans text from HTML content using `BeautifulSoup4`.

**Installation:**
```bash
pip install "generic-rag[html]"
```
Note: If the extra is not installed, instantiating the loader will raise a `ConfigurationError`.

**Usage:**
```python
from generic_rag.ingestion.html import HTMLDocumentLoader
loader = HTMLDocumentLoader()
docs = await loader.load("path/to/file.html")
# Or directly from a string:
# docs = await loader.load("<html><body>...</body></html>")
```

**Features & Limitations:**
- **No Fetching:** The loader only processes local files or in-memory strings. It does **not** perform HTTP requests (crawling).
- **Basic Cleaning:** Removes `<script>`, `<style>`, `<nav>`, `<footer>`, `<aside>`, `<header>`, and `<noscript>` tags before extracting text.
- **No Advanced Tables/Images:** Extracts text linearly, discarding complex visual layout.

## Pipeline Example: Loader + Chunker

Loaders produce `Document`s, which are then passed to a `Chunker` before embedding. The chunker automatically preserves `SourceRef` metadata (like the PDF page number or HTML title) so that citations remain accurate.

```python
import asyncio
from generic_rag.ingestion.pdf import PyMuPDFDocumentLoader
from generic_rag.ingestion.chunkers import CharacterChunker

async def main():
    # 1. Load the document
    loader = PyMuPDFDocumentLoader()
    docs = await loader.load("sample.pdf")
    
    # 2. Chunk the documents
    chunker = CharacterChunker(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.split_documents(docs)
    
    print(f"Created {len(chunks)} chunks.")
    # Each chunk has chunk.source.page preserving the original page!

asyncio.run(main())
```
