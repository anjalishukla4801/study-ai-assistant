import streamlit as st
from sentence_transformers import SentenceTransformer

class RAGEmbeddings:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                self._model = self._load_model(self.model_name)
            except Exception as e:
                raise RuntimeError(f"Failed to load embedding model '{self.model_name}': {str(e)}")
        return self._model

    @staticmethod
    @st.cache_resource
    def _load_model(model_name):
        # This will download the model on the first call and cache it in memory
        return SentenceTransformer(model_name)

    def embed_documents(self, texts: list) -> list:
        """
        Generates embeddings for a list of document strings.
        """
        try:
            if not texts:
                return []
            embeddings = self.model.encode(texts, show_progress_bar=False)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            raise RuntimeError(f"Error generating document embeddings: {str(e)}")

    def embed_query(self, text: str) -> list:
        """
        Generates embedding for a query string.
        """
        try:
            embedding = self.model.encode(text, show_progress_bar=False)
            return embedding.tolist()
        except Exception as e:
            raise RuntimeError(f"Error generating query embedding: {str(e)}")
