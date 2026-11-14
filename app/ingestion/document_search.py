
import os

import numpy as np
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

from app.semantic_search import get_model

load_dotenv()


def search_documents(query: str, top_k: int = 5) -> list[dict]:
    """Search PDF chunks using pgvector cosine similarity."""

    if not query.strip():
        return []

    if top_k < 1:
        raise ValueError("top_k must be positive")

    # Convert the user's question into an embedding
    session, tokenizer = get_model()

    inputs = tokenizer(
        query,
        return_tensors="np",
        truncation=True,
        max_length=256,
    )

    onnx_inputs = {
        item.name: inputs[item.name]
        for item in session.get_inputs()
    }

    query_embedding = session.run(
        ["sentence_embedding"],
        onnx_inputs,
    )[0][0].astype(np.float32)

    # Search stored PDF embeddings
    with psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        dbname="tactictrail",
        user="tactictrail",
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    ) as connection:
        register_vector(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    document,
                    page,
                    heading,
                    chunk_id,
                    text,
                    1 - (embedding <=> %s) AS similarity_score
                FROM document_chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (query_embedding, query_embedding, top_k),
            )

            rows = cursor.fetchall()

    return [
        {
            "document": row[0],
            "page": row[1],
            "heading": row[2],
            "chunk_id": row[3],
            "text": row[4],
            "similarity_score": float(row[5]),
        }
        for row in rows
    ]
