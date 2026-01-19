# === README.md ===
# AI Log Analyzer (Offline - GPT4All Edition)

🚀 A fully offline, private, and intelligent AI-powered log file analyzer that can answer user-defined questions and summarize logs using local models (no API keys needed).

## Features
- 🔍 Analyze and understand logs
- 🧠 Ask multiple questions at once
- ⚙️ Powered by local GPT4All models

## Folder Structure
```
AI_log_analyzer/
├── app/
│   ├── main.py
│   ├── log_parser.py
│   ├── summarizer.py
│   ├── vector_store.py
│   ├── query_engine.py
│   └── utils.py
├── models/
│   └── gpt4all-model.bin/mistral-7b-openorca.Q4_0.gguf
├── data/
│   └── logs/
├── requirements.txt
├── README.md
└── run.py
```

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download GPT4All Model
```bash
git clone https://github.com/nomic-ai/gpt4all.git
cd gpt4all
add mistral-7b-openorca.Q4_0.gguf model in gpt4all/models/mistral-7b-openorca.Q4_0.gguf
pip install -r requirements.txt
python download_model.py  # or manually download model file
```
Move model to project folder:
```bash
mv ~/Downloads/gpt4all-model.bin ../AI_log_analyzer/models/
```

### 3. Run the App
```bash
cd ../AI_log_analyzer
python run.py
```

