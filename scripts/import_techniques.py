
import json
import os
from pathlib import Path

import numpy as np
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env")

DATA_FILE = ROOT / "data/raw/enterprise_techniques.json"
EMBEDDINGS_FILE = ROOT / "data/embeddings/technique_embeddings.npy"


def import_techniques():
    # Load existing MITRE techniques and embeddings
    with DATA_FILE.open(encoding="utf-8") as file:
        techniques = json.load(file)

    embeddings = np.load(EMBEDDINGS_FILE, allow_pickle=False)

    # Validate data before importing
    if embeddings.shape != (len(techniques), 384):
        raise ValueError("Technique count or embedding dimensions do not match")

    ids = [technique["technique_id"] for technique in techniques]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate MITRE technique IDs found")

    if not np.isfinite(embeddings).all():
        raise ValueError("Embeddings contain invalid values")

    password = os.getenv("POSTGRES_PASSWORD")
    if not password:
        raise RuntimeError("POSTGRES_PASSWORD missing from .env")

    # Connect to local PostgreSQL Docker container
    with psycopg.connect(
        host="127.0.0.1",
        port=5433,
        dbname="tactictrail",
        user="tactictrail",
        password=password,
    ) as connection:
        register_vector(connection)

        rows = [
            (
                technique["technique_id"],
                technique["name"],
                technique.get("description"),
                technique.get("url"),
                embeddings[i].astype(np.float32),
            )
            for i, technique in enumerate(techniques)
        ]

        with connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO mitre_techniques
                    (technique_id, name, description, url, embedding)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (technique_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    url = EXCLUDED.url,
                    embedding = EXCLUDED.embedding
                """,
                rows,
            )

    print(f"Successfully imported {len(rows)} MITRE techniques!")


if __name__ == "__main__":
    import_techniques()
