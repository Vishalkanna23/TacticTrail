
from types import SimpleNamespace

import numpy as np

from app.ingestion import embedder


def test_embed_chunks_preserves_metadata(monkeypatch):
    class FakeSession:
        def get_inputs(self):
            return [SimpleNamespace(name="input_ids")]

        def run(self, outputs, inputs):
            return [
                np.ones((1, 384), dtype=np.float32)
            ]

    def fake_tokenizer(
        text,
        return_tensors,
        truncation=False,
        max_length=None,
    ):
        assert truncation is True
        assert max_length == 256

        return {
            "input_ids": np.array([[1, 2, 3]])
        }

    monkeypatch.setattr(
        embedder,
        "get_model",
        lambda: (FakeSession(), fake_tokenizer),
    )

    chunks = [
        {
            "chunk_id": 0,
            "document": "security.pdf",
            "page": 5,
            "heading": "Credential Access",
            "text": "Brute force attacks involve password guessing.",
        }
    ]

    result = embedder.embed_chunks(chunks)

    assert len(result) == 1
    assert result[0]["document"] == "security.pdf"
    assert result[0]["page"] == 5
    assert result[0]["heading"] == "Credential Access"
    assert result[0]["embedding"].shape == (384,)
