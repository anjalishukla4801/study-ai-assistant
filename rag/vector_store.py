import os
import chromadb

class RAGVectorStore:
    def __init__(self, persist_directory="vector_db"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        try:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ChromaDB PersistentClient: {str(e)}")

    def _get_collection_name(self, pdf_hash: str) -> str:
        # Safe collection name: 'pdf_' + first 48 chars of hash
        return f"pdf_{pdf_hash[:48]}"

    def collection_exists_and_populated(self, pdf_hash: str) -> bool:
        """
        Checks if a collection exists and has document embeddings.
        """
        try:
            name = self._get_collection_name(pdf_hash)
            collections = [col.name for col in self.client.list_collections()]
            if name in collections:
                col = self.client.get_collection(name)
                return col.count() > 0
            return False
        except Exception:
            return False

    def get_or_create_collection(self, pdf_hash: str):
        """
        Retrieves or creates a ChromaDB collection for a given PDF hash.
        """
        try:
            name = self._get_collection_name(pdf_hash)
            return self.client.get_or_create_collection(name=name)
        except Exception as e:
            raise RuntimeError(f"ChromaDB error getting/creating collection: {str(e)}")

    def add_chunks(self, pdf_hash: str, chunks: list, embeddings: list):
        """
        Saves chunks, their corresponding metadata and embeddings to ChromaDB.
        """
        try:
            collection = self.get_or_create_collection(pdf_hash)
            
            ids = [f"chunk_{item['metadata']['chunk_number']}" for item in chunks]
            documents = [item['text'] for item in chunks]
            metadatas = [item['metadata'] for item in chunks]
            
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
        except Exception as e:
            raise RuntimeError(f"Failed to save embeddings to ChromaDB: {str(e)}")

    def query(self, pdf_hash: str, query_embedding: list, top_k=5) -> list:
        """
        Queries ChromaDB for the closest document chunks.
        """
        try:
            name = self._get_collection_name(pdf_hash)
            collections = [col.name for col in self.client.list_collections()]
            if name not in collections:
                return []
                
            collection = self.client.get_collection(name)
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            retrieved = []
            if results and 'documents' in results and results['documents'] and len(results['documents']) > 0:
                docs = results['documents'][0]
                metas = results['metadatas'][0] if 'metadatas' in results else []
                
                for i in range(len(docs)):
                    retrieved.append({
                        "text": docs[i],
                        "metadata": metas[i] if i < len(metas) else {}
                    })
                    
            return retrieved
        except Exception as e:
            raise RuntimeError(f"ChromaDB search query failed: {str(e)}")

    def get_all_chunks(self, pdf_hash: str) -> list:
        """
        Retrieves all documents and metadatas in the collection for the given pdf_hash.
        Returns a list of dictionaries: [{"text": doc, "metadata": meta}]
        """
        try:
            name = self._get_collection_name(pdf_hash)
            collections = [col.name for col in self.client.list_collections()]
            if name not in collections:
                return []
                
            collection = self.client.get_collection(name)
            results = collection.get(include=["documents", "metadatas"])
            
            chunks = []
            if results and 'documents' in results and results['documents']:
                docs = results['documents']
                metas = results['metadatas']
                for i in range(len(docs)):
                    chunks.append({
                        "text": docs[i],
                        "metadata": metas[i] if i < len(metas) else {}
                    })
                    
            # Sort by chunk_number to maintain document order
            chunks.sort(key=lambda x: x["metadata"].get("chunk_number", 0))
            return chunks
        except Exception as e:
            raise RuntimeError(f"Failed to fetch chunks from ChromaDB: {str(e)}")
