from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGChunker:
    def __init__(self, chunk_size=700, chunk_overlap=150):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def chunk_documents(self, pages: list) -> list:
        """
        Chunks a list of pages and attaches metadata.
        Returns a list of dictionaries:
        {
            "text": str,
            "metadata": {
                "filename": str,
                "page_number": int,
                "chunk_number": int,
                "chunk_text": str
            }
        }
        """
        chunks = []
        global_chunk_idx = 1
        
        for page in pages:
            page_text = page["text"]
            page_num = page["page_number"]
            filename = page["filename"]
            
            if not page_text.strip():
                continue
                
            page_chunks = self.text_splitter.split_text(page_text)
            
            for chunk_text in page_chunks:
                chunk_text = chunk_text.strip()
                if not chunk_text:
                    continue
                    
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "filename": filename,
                        "page_number": page_num,
                        "chunk_number": global_chunk_idx,
                        "chunk_text": chunk_text
                    }
                })
                global_chunk_idx += 1
                
        return chunks
