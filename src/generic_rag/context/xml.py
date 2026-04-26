from html import escape
from typing import List
from generic_rag.core.schemas import ScoredChunk, ContextOptions
from generic_rag.context.builder import BaseContextBuilder

class XMLContextBuilder(BaseContextBuilder):
    def build_context(self, chunks: List[ScoredChunk], options: ContextOptions) -> str:
        parts = ["<context>"]
        
        # very naive token counting approximation: 1 token ~ 4 chars
        current_length = 0
        max_chars = options.max_tokens * 4
        
        for chunk in chunks:
            doc_tag = f'<document chunk_id="{escape(chunk.id)}" document_id="{escape(chunk.document_id)}" score="{chunk.score:.4f}">'
            
            source_tag = ""
            if options.include_metadata and chunk.source:
                attrs = []
                if chunk.source.title:
                    attrs.append(f'title="{escape(chunk.source.title)}"')
                if chunk.source.uri:
                    attrs.append(f'uri="{escape(chunk.source.uri)}"')
                if chunk.source.page is not None:
                    attrs.append(f'page="{chunk.source.page}"')
                if chunk.source.section:
                    attrs.append(f'section="{escape(chunk.source.section)}"')
                
                if attrs:
                    source_tag = f'  <source {" ".join(attrs)} />\n'
                    
            content_tag = f"  <content>{escape(chunk.content)}</content>"
            doc_end = "</document>"
            
            chunk_xml = f"{doc_tag}\n{source_tag}{content_tag}\n{doc_end}"
            
            if current_length + len(chunk_xml) > max_chars and current_length > 0:
                # Stop adding chunks if we exceed approximate max chars
                # We add at least one chunk even if it exceeds the limit (unless we want to hard trim)
                break
                
            parts.append(chunk_xml)
            current_length += len(chunk_xml)
            
        parts.append("</context>")
        return "\n".join(parts)
