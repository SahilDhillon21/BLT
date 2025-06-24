import json

import numpy as np


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return np.dot(a, b) / (norm_a * norm_b)


def get_embedding(item):
    """Extract the embedding list from an item."""
    emb = item.get("embedding")
    if isinstance(emb, dict):
        return emb.get("embedding")
    return emb


def main():
    try:
        with open("embeddings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading embeddings.json: {e}")
        return
    grouped = {}
    for item in data:
        content_type = item["content"]["type"]
        embedding = get_embedding(item)

        if embedding is not None:
            if content_type not in grouped:
                grouped[content_type] = []
            grouped[content_type].append((item, embedding))

    for content_type, items in grouped.items():
        if len(items) >= 2:
            (item1, emb1), (item2, emb2) = items[:2]
            sim = cosine_similarity(emb1, emb2)
            print(f"Similarity for type '{content_type}': {sim:.4f}")
            print(f"  '{item1['content']['chunk'][:60]}...' vs '{item2['content']['chunk'][:60]}...'")

    import_item = grouped.get("import")
    function_item = grouped.get("function")

    if import_item and function_item:
        (item1, emb1) = import_item[0]
        (item2, emb2) = function_item[0]
        sim = cosine_similarity(emb1, emb2)
        print(f"\nSimilarity between first import and first function: {sim:.4f}")
        print(f"  '{item1['content']['chunk'][:60]}...' vs '{item2['content']['chunk'][:60]}...'")
    else:
        print("\nNot enough data to compare import and function chunks.")


if __name__ == "__main__":
    main()
