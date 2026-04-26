# Requires: pip install -e ".[html]"

import asyncio
from generic_rag.ingestion.html import HTMLDocumentLoader

async def main():
    # Usaremos contenido en memoria para este ejemplo
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Artículo de Prueba</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .hidden { display: none; }
        </style>
        <script>
            console.log("Este script debe ser ignorado por el loader");
        </script>
    </head>
    <body>
        <header>
            <h1>Mi Blog</h1>
            <nav>
                <ul>
                    <li><a href="/">Inicio</a></li>
                    <li><a href="/about">Acerca de</a></li>
                </ul>
            </nav>
        </header>

        <main>
            <article>
                <h2>Introducción a generic-rag</h2>
                <p>
                    Generic-rag es una librería <strong>agnóstica</strong> y ligera para 
                    orquestación de LLMs y pipelines RAG.
                </p>
                <p>
                    En la versión 0.5.0, hemos añadido soporte opcional para parsear 
                    HTML y PDF sin inflar las dependencias base.
                </p>
            </article>
            
            <aside>
                <h3>Publicidad</h3>
                <p>¡Compra nuestros productos!</p>
            </aside>
        </main>

        <footer>
            <p>&copy; 2026 generic-rag</p>
        </footer>
    </body>
    </html>
    """
    
    print("Cargando HTML de prueba en memoria...")
    loader = HTMLDocumentLoader()
    
    try:
        documents = await loader.load(html_content)
        
        print(f"\nSe cargó {len(documents)} documento.")
        doc = documents[0]
        
        print("\n--- Detalles del Documento ---")
        print(f"ID: {doc.id}")
        print(f"Source Type: {doc.source.source_type}")
        print(f"Title: {doc.source.title}")
        print(f"URI: {doc.source.uri}")
        print("\n--- Contenido Extraído ---")
        print(doc.content)

    except ImportError as e:
        print(f"\nError de importación: {e}")
        print("Instala las dependencias opcionales con: pip install -e \".[html]\"")
    except Exception as e:
        print(f"\nError al cargar: {e}")

if __name__ == "__main__":
    asyncio.run(main())
