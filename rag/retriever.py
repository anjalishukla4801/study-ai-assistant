from rag.embeddings import RAGEmbeddings
from rag.vector_store import RAGVectorStore

class RAGRetriever:
    def __init__(self, embeddings: RAGEmbeddings, vector_store: RAGVectorStore):
        self.embeddings = embeddings
        self.vector_store = vector_store

    def retrieve(self, pdf_hash: str, query: str, top_k=5) -> list:
        """
        Retrieves the top_k most relevant chunks for a query from the database.
        """
        if not query.strip():
            return []
            
        try:
            query_embedding = self.embeddings.embed_query(query)
            results = self.vector_store.query(pdf_hash, query_embedding, top_k=top_k)
            return results
        except Exception as e:
            raise RuntimeError(f"Retrieval process failed: {str(e)}")

    def get_diverse_chunks(self, pdf_hash: str, num_chunks=8) -> list:
        """
        Fetches all chunks and returns a sample of num_chunks evenly distributed 
        across the document to represent all parts (beginning, middle, end).
        """
        all_chunks = self.vector_store.get_all_chunks(pdf_hash)
        if not all_chunks:
            return []
            
        n = len(all_chunks)
        if n <= num_chunks:
            return all_chunks
            
        # Select evenly spaced indices
        indices = [int(i * (n - 1) / (num_chunks - 1)) for i in range(num_chunks)]
        # Remove duplicates just in case
        indices = sorted(list(set(indices)))
        
        return [all_chunks[idx] for idx in indices]
