# === app/vector_store.py ===
import faiss
import numpy as np

class LogVectorStore:
    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatL2(dimension)
        self.text_chunks = []

    def add(self, vectors, chunks):
        self.index.add(np.array(vectors).astype('float32'))
        self.text_chunks.extend(chunks)

    def search(self, query_vector, top_k=5):
        D, I = self.index.search(np.array([query_vector]).astype('float32'), top_k)
        return [self.text_chunks[i] for i in I[0]]
