
import json
from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer, util

from app import technique_search
from app.build_embeddings import EMBEDDINGS_FILE, MODEL_NAME

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)
def search_semantic(query, top_k=5):
    if not query.strip():
        return []

    with open(technique_search.DATA_FILE, encoding="utf-8") as file:
        techniques = json.load(file)

    if not techniques:
        return []

    # Load the embeddings we generated earlier
    document_embeddings = np.load(EMBEDDINGS_FILE)

    if len(document_embeddings) != len(techniques):
        raise ValueError(
            "Embedding count does not match the MITRE dataset. "
            "Run python -m app.build_embeddings again."
        )

    # Load the model and encode only the user's query
    model = get_model()

    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    # Compare the query against the saved embeddings
    scores = util.cos_sim(query_embedding, document_embeddings)[0]

    ranked_indices = scores.argsort(descending=True)[:top_k]

    results = []

    for index in ranked_indices:
        technique = techniques[index.item()].copy()
        technique["similarity_score"] = float(scores[index].item())
        results.append(technique)

    return results


if __name__ == "__main__":
    results = search_semantic("How do hackers steal passwords?")

    for technique in results:
        print(
            technique["technique_id"],
            technique["name"],
            round(technique["similarity_score"], 3),
        )
