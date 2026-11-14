
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Store PDF chunks and their embeddings
CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,

    document TEXT NOT NULL,
    page INTEGER NOT NULL CHECK (page >= 1),
    heading TEXT,

    chunk_id INTEGER NOT NULL,
    text TEXT NOT NULL,

    embedding VECTOR(384),

    UNIQUE (document, chunk_id)
);
