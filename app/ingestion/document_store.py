
import os

import numpy as np
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

load_dotenv()


def save_document_chunks(chunks: list[dict]) -> int:
    """Save embedded PDF chunks in PostgreSQL."""

    if not chunks:
        return 0

    rows = []

    for chunk in chunks:
        embedding = np.asarray(
            chunk["embedding"],
            dtype=np.float32,
        )

        if embedding.shape != (384,):
            raise ValueError(
                "Embedding must have 384 dimensions"
            )

        if not np.isfinite(embedding).all():
            raise ValueError(
                "Embedding contains invalid numbers"
            )

        rows.append(
            (
                chunk["document"],
                chunk["page"],
                chunk.get("heading"),
                chunk["chunk_id"],
                chunk["text"],
                embedding,
            )
        )

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
            cursor.executemany(
                """
                INSERT INTO document_chunks (
                    document,
                    page,
                    heading,
                    chunk_id,
                    text,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (document, chunk_id)
                DO UPDATE SET
                    page = EXCLUDED.page,
                    heading = EXCLUDED.heading,
                    text = EXCLUDED.text,
                    embedding = EXCLUDED.embedding
                """,
                rows,
            )

    return len(rows)
