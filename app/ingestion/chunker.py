
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[dict]:
    """Split extracted PDF pages into overlapping text chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    chunk_id = 0

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "document": page["document"],
                    "page": page["page"],
                    "heading": page.get("heading"),
                    "text": text[start:end],
                }
            )

            chunk_id += 1

            if end == len(text):
                break

            start = end - overlap

    return chunks
