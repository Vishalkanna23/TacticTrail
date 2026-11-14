import numpy as np

from app.semantic_search import get_model


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Generate 384-dimensional embeddings for PDF chunks."""

    if not chunks:
        return []

    # Load the existing ONNX embedding model
    session, tokenizer = get_model()

    embedded_chunks = []

    for chunk in chunks:
        # Convert text into model inputs
        inputs = tokenizer(
            chunk["text"],
            return_tensors="np",
            truncation=True,
            max_length=256,
        )

        onnx_inputs = {item.name: inputs[item.name] for item in session.get_inputs()}

        # Generate a 384-dimensional embedding
        embedding = session.run(
            ["sentence_embedding"],
            onnx_inputs,
        )[0][0].astype(np.float32)

        if embedding.shape != (384,):
            raise ValueError("Expected a 384-dimensional embedding")

        if not np.isfinite(embedding).all():
            raise ValueError("Embedding contains invalid numbers")

        embedded_chunks.append(
            {
                **chunk,
                "embedding": embedding,
            }
        )

    return embedded_chunks
