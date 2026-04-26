# Requires: pip install -e ".[pdf]"

import asyncio
import sys
from pathlib import Path
from generic_rag.ingestion.pdf import PyMuPDFDocumentLoader

async def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("Uso: python pdf_loader.py <ruta_al_pdf>")
        print("Proporciona una ruta local a un archivo PDF para probar el loader.")
        print("Ejemplo: python pdf_loader.py documento.pdf")
        return

    path = Path(pdf_path)
    if not path.exists():
        print(f"Error: El archivo {pdf_path} no existe.")
        return

    print(f"Cargando {pdf_path}...")
    loader = PyMuPDFDocumentLoader()
    
    try:
        documents = await loader.load(path)
        
        print(f"\nSe cargaron {len(documents)} documentos (páginas).")
        
        for i, doc in enumerate(documents[:3]):  # Mostrar max 3 páginas
            print(f"\n--- Documento {i+1} ---")
            print(f"ID: {doc.id}")
            print(f"Source Type: {doc.source.source_type}")
            print(f"Title: {doc.source.title}")
            print(f"Page: {doc.source.page}")
            print(f"Preview: {doc.content[:150]}...")
            
        if len(documents) > 3:
            print(f"\n... y {len(documents) - 3} páginas más omitidas.")

    except ImportError as e:
        print(f"\nError de importación: {e}")
        print("Instala las dependencias opcionales con: pip install -e \".[pdf]\"")
    except Exception as e:
        print(f"\nError al cargar: {e}")

if __name__ == "__main__":
    asyncio.run(main())
