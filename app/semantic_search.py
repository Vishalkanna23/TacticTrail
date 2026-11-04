
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

from app import technique_search

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "minilm-onnx"
EMBEDDINGS_FILE = BASE_DIR / "data" / "embeddings" / "technique_embeddings.npy"


@lru_cache(maxsize=1)
def get_model():
    session = ort.InferenceSession(
        str(MODEL_DIR / "model.onnx"),
        providers=["CPUExecutionProvider"],
    )
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    return session, tokenizer


def search_semantic(query, top_k=5):
    if not query.strip():
        return []

    with open(technique_search.DATA_FILE, encoding="utf-8") as file:
        techniques = json.load(file)

    if not techniques:
        return []

    document_embeddings = np.load(EMBEDDINGS_FILE)

    if len(document_embeddings) != len(techniques):
        raise ValueError(
            "Embedding count does not match the MITRE dataset. "
            "Run python -m app.build_embeddings again."
        )

    # Generate the query embedding using ONNX Runtime
    session, tokenizer = get_model()

    inputs = tokenizer(query, return_tensors="np")

    onnx_inputs = {
        item.name: inputs[item.name]
        for item in session.get_inputs()
    }

    query_embedding = session.run(
        ["sentence_embedding"],
        onnx_inputs,
    )[0][0]

    # Compare normalized query and document embeddings
    scores = document_embeddings @ query_embedding

    # Rank techniques by similarity
    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        technique = techniques[int(index)].copy()
        technique["similarity_score"] = float(scores[index])
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
