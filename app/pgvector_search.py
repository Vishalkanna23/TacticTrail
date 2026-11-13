
import os

import numpy as np
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

from app.semantic_search import get_model

load_dotenv()


def search_pgvector(query: str, top_k: int = 5):
    if not query.strip():
        return []

    # Convert the question into a 384-dimensional vector
    session, tokenizer = get_model()
    inputs = tokenizer(query, return_tensors="np")

    onnx_inputs = {
        item.name: inputs[item.name]
        for item in session.get_inputs()
    }

    query_embedding = session.run(
        ["sentence_embedding"],
        onnx_inputs,
    )[0][0].astype(np.float32)

    # Database settings:
    # Windows: 127.0.0.1:5433
    # Docker: tactictrail-db:5432
    db_host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    db_port = int(os.getenv("POSTGRES_PORT", "5433"))

    # Connect to PostgreSQL
    with psycopg.connect(
        host=db_host,
        port=db_port,
        dbname="tactictrail",
        user="tactictrail",
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    ) as connection:
        register_vector(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT technique_id, name, description, url,
                       1 - (embedding <=> %s) AS similarity_score
                FROM mitre_techniques
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (query_embedding, query_embedding, top_k),
            )

            rows = cursor.fetchall()

    return [
        {
            "technique_id": row[0],
            "name": row[1],
            "description": row[2],
            "url": row[3],
            "similarity_score": float(row[4]),
        }
        for row in rows
    ]
