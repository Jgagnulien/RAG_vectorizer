# main.py
from utils.to_json import generate_json_from_excels
from utils.preprocess import vectorize_documents, search
import os

# Paths
folder_path = "C:/Users/jugagn/OneDrive - SAS/Documents/vscode/agentic_ai/.venv/data/rules_active"
vector_json = "docs_vector.json"
metadata_json = "docs_metadata.json"

# Step 1: Generate JSON if needed
generate_json_from_excels(folder_path, vector_json, metadata_json)

# Step 2: Load/cached vectorization
X, vectorizer = vectorize_documents(vector_json)

# Step 3: Query
query = input("Query : ")
top_k = 5
results = search(query, vectorizer, X, vector_json, top_k)

# Step 4: Output
print(f"/n📄 Top {top_k} results:")
for i, res in enumerate(results, 1):
    print(f"/n#{i} (score: {res['score']:.4f})")
    print(f"Key: {res['key']}")