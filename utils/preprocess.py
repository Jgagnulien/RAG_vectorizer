# utils/preprocess.py

import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import scipy.sparse
import os
from datetime import datetime
import hashlib


def compute_file_hash(filepath):
    """
    Compute the SHA256 hash of a file.

    Args:
        filepath (str): Path to the file to hash.

    Returns:
        str: SHA256 hash of the file as a hexadecimal string.
    """
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def vectorize_documents(docs_path, cache_dir="cache"):
    """
    Vectorize the text content of a JSON file using the Bag-of-Words model.
    Caches the results to avoid redundant computation if the document content hasn't changed.

    Args:
        docs_path (str): Path to the JSON file containing a list of documents with a "text" field.
        cache_dir (str, optional): Directory to store cached vectorizer and matrix files. Defaults to "cache".

    Returns:
        tuple:
            - scipy.sparse.csr_matrix: Document-term matrix.
            - CountVectorizer: Fitted vectorizer instance.
    """
    os.makedirs(cache_dir, exist_ok=True)

    vectorizer_path = os.path.join(cache_dir, "vectorizer.pkl")
    matrix_path = os.path.join(cache_dir, "X.npz")
    hash_path = os.path.join(cache_dir, "docs.hash")

    current_hash = compute_file_hash(docs_path)

    # Check if the cached data is still valid
    cache_valid = (
        os.path.exists(vectorizer_path) and
        os.path.exists(matrix_path) and
        os.path.exists(hash_path) and
        open(hash_path).read().strip() == current_hash
    )

    if cache_valid:
        print("✅ Using cached vectorized data.")
        vectorizer = joblib.load(vectorizer_path)
        X = scipy.sparse.load_npz(matrix_path)
    else:
        print("🔄 Re-vectorizing documents due to content change...")
        with open(docs_path, "r", encoding="utf-8") as f:
            docs = json.load(f)
        texts = [doc["text"] for doc in docs]

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(texts)

        # Save to cache
        joblib.dump(vectorizer, vectorizer_path)
        scipy.sparse.save_npz(matrix_path, X)
        with open(hash_path, "w") as f:
            f.write(current_hash)

        print("✅ Vectorization complete and cache updated.")

    return X, vectorizer


def search(query, vectorizer, X, docs_path, top_k=5, save_path="search_results.json"):
    """
    Search for the most relevant documents based on cosine similarity with a given query.

    Args:
        query (str): The user's search query.
        vectorizer (CountVectorizer): Fitted CountVectorizer used to transform the query.
        X (scipy.sparse.csr_matrix): Document-term matrix of the original documents.
        docs_path (str): Path to the original JSON file containing documents.
        top_k (int, optional): Number of top matching documents to return. Defaults to 5.
        save_path (str, optional): Base path to save the search results (timestamped). Defaults to "search_results.json".

    Returns:
        list: A list of the top matching document dictionaries with an added "score" field.
    """
    # Load the original documents
    with open(docs_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Vectorize the query
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, X).flatten()
    top_indices = similarities.argsort()[::-1][:top_k]

    # Prepare the results with similarity scores
    results = [docs[i] | {"score": float(similarities[i])} for i in top_indices]

    # Create output with query and results
    output_data = [{"query": query}] + results

    # Save results with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"{os.path.splitext(save_path)[0]}_{timestamp}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Search results saved to {out_file}")

     # ✅ Count words in output file
    total_words = sum(len(str(value).split()) for item in output_data for value in item.values())

    print(f"📝 Total word count in output: {total_words}")

    return results
