
# 📚 Semantic Search Engine for JSON Documents

This project provides a simple and efficient way to **vectorize text documents**, **cache results**, and perform **semantic search** using the Bag-of-Words model and cosine similarity. It is ideal for lightweight search applications across rulebooks, policies, or any structured JSON content.

## 🔧 Features

- Text vectorization using `CountVectorizer` (Bag-of-Words)
- Automatic caching based on file hash to avoid re-processing
- Cosine similarity search across document vectors
- Timestamped export of search results
- Clean and modular Python code

---

## 📁 Project Structure

```
.
├── utils/
│   └── preprocess.py       # Core logic for vectorization and search
├── data/
│   └── rules.json          # Example input file with text documents
├── cache/                  # Cached vectorizer and matrix files
├── results/                # Saved search results
└── README.md
```

---

## 🧩 Requirements

Install the required Python packages using:

```bash
pip install scikit-learn joblib
```

---

## 📄 Input Format

The input file (`rules.json`, for example) must be a **JSON list of documents**, each with at least a `"text"` field:

```json
[
  {
    "id": 1,
    "title": "Rule A",
    "text": "This rule applies to financial operations."
  },
  {
    "id": 2,
    "title": "Rule B",
    "text": "Applicable to all investment accounts."
  }
]
```

---

## 🚀 Usage

### 1. Vectorize Documents

```python
from utils.preprocess import vectorize_documents

X, vectorizer = vectorize_documents("data/rules.json")
```

This will:
- Vectorize the `text` field in your JSON file
- Cache the vectorizer and matrix in `cache/`
- Automatically re-use cache if the file hasn't changed

---

### 2. Run a Search

```python
from utils.preprocess import search

results = search(
    query="investment policy",
    vectorizer=vectorizer,
    X=X,
    docs_path="data/rules.json"
)
```

This will:
- Compute similarity between your query and all documents
- Return the top 5 matches
- Save a timestamped `.json` file with the results

---

## 💾 Output Format

The saved search result file will look like:

```json
[
  {
    "query": "investment policy"
  },
  {
    "id": 2,
    "title": "Rule B",
    "text": "Applicable to all investment accounts.",
    "score": 0.4898
  }
]
```

---

## 📌 Notes

- You can adjust the number of returned results via the `top_k` parameter.
- Change the `cache_dir` and `save_path` if needed for more flexible I/O management.

---

## 🛠️ TODOs / Improvements

- Switch to `TfidfVectorizer` for better ranking
- Add command-line interface (CLI)
- Support more advanced models (e.g., embeddings via `sentence-transformers`)

---

## 📝 License

MIT License. Feel free to use, modify, and contribute.
