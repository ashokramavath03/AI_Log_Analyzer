# === app/query_engine.py ===
from sentence_transformers import SentenceTransformer
from vector_store import LogVectorStore
from summarizer import Summarizer
from utils import normalize_text, extract_keywords

class QueryEngine:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_store = LogVectorStore()
        self.summarizer = Summarizer()
        self.raw_log_lines = []

    def index_logs(self, chunks, raw_lines):
        normalized_chunks = [normalize_text(chunk) for chunk in chunks]
        vectors = self.embedder.encode(normalized_chunks)
        self.vector_store.add(vectors, chunks)
        self.raw_log_lines = raw_lines

    def search_logs(self, question):
        keyword_query = extract_keywords(question)
        return [
            line for line in self.raw_log_lines
            if keyword_query in normalize_text(line)
        ]

    def answer_queries(self, questions):
        results = []
        for q in questions:
            matches = self.search_logs(q)
            context = "\n".join(matches[:5])
            if not context:
                context = "No direct matches found in logs. Try broader keywords."
            answer = self.summarizer.summarize(context, q)
            results.append({
                "question": q,
                "matched_logs": matches[:5],
                "answer": answer.strip()
            })
        return results
