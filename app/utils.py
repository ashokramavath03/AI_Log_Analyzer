import re
import nltk
from nltk.stem import WordNetLemmatizer
from symspellpy.symspellpy import SymSpell, Verbosity
import os

nltk.download("wordnet", quiet=True)
lemmatizer = WordNetLemmatizer()

# Setup SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2)
dict_path = os.path.join(os.path.dirname(__file__), "..", "data", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)

def split_logs_by_lines(log_data):
    return log_data.strip().splitlines()

def extract_timestamped_chunks(log_lines, window_size=5):
    for i in range(0, len(log_lines), window_size):
        yield "\n".join(log_lines[i:i+window_size])

def normalize_text(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return " ".join([lemmatizer.lemmatize(token) for token in tokens])

def autocorrect(text):
    tokens = text.strip().split()
    corrected = []
    for token in tokens:
        suggestions = sym_spell.lookup(token, Verbosity.CLOSEST, max_edit_distance=2)
        corrected.append(suggestions[0].term if suggestions else token)
    return " ".join(corrected)

def extract_keywords(question):
    corrected = autocorrect(question)
    return normalize_text(corrected)
