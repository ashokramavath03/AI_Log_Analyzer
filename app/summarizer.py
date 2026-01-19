# === app/summarizer.py ===
import os
from llama_cpp import Llama

class Summarizer:
    def __init__(self, model_filename="mistral-7b-openorca.Q4_0.gguf"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        model_path = os.path.join(project_root, "models", model_filename)

        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        self.model = Llama(
            model_path=model_path,
            n_ctx=1024,       # Reduce context window for performance
            n_threads=2,      # Tune based on your VM (e.g. 2 cores)
            use_mlock=True,   # Keeps model in memory to avoid swap
        )

    def summarize(self, context, question, max_context_chars=800):
        # Truncate long logs for speed and token limit
        if len(context) > max_context_chars:
            context = context[:max_context_chars]

        prompt = f"""You are an expert in system log analysis.

### Context:
{context}

### Question:
{question}

### Answer:
"""
        response = self.model(prompt, max_tokens=256, temperature=0.3, stop=["###"])
        return response["choices"][0]["text"].strip()
