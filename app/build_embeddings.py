
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from app import technique_search

EMBEDDINGS_FILE = Path("data/embeddings/technique_embeddings.npy")
MODEL_NAME = "all-MiniLM-L6-v2"


def build_embeddings():
    with open(technique_search.DATA_FILE, encoding="utf-8") as file:
        techniques = json.load(file)

    if not techniques:
        print("No MITRE techniques found.")
        return

    documents = [
        technique["name"] + " " + technique["description"]
        for technique in techniques
    ]

    print(f"Generating embeddings for {len(documents)} techniques...")

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    EMBEDDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_FILE, embeddings)

    print(f"Saved embeddings to {EMBEDDINGS_FILE}")
    print(f"Embedding shape: {embeddings.shape}")


if __name__ == "__main__":
    build_embeddings()
