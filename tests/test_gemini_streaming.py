
from types import SimpleNamespace

from google.genai import errors

from app import gemini_service


def test_stream_interrupted_after_partial_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    models_called = []

    def fake_stream(*, model, contents):
        models_called.append(model)

        yield SimpleNamespace(
            text="Brute force involves guessing passwords."
        )

        raise errors.ServerError(
            503,
            {"message": "High demand"},
        )

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=fake_stream
        )
    )

    monkeypatch.setattr(
        gemini_service.genai,
        "Client",
        lambda **kwargs: fake_client,
    )

    chunks = list(
        gemini_service.stream_answer(
            "Explain brute force attacks",
            "T1110 - Brute Force",
        )
    )

    assert "guessing passwords" in chunks[0]
    assert "incomplete" in chunks[-1].lower()

    # Do not restart with another model after text was sent
    assert models_called == ["gemini-3.5-flash-lite"]

def test_stream_fallback_before_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    models_called = []

    def fake_stream(*, model, contents):
        models_called.append(model)

        if model == "gemini-3.5-flash-lite":
            raise errors.ServerError(
                503,
                {"message": "High demand"},
            )

        yield SimpleNamespace(
            text="T1110 is a brute force technique.",
            usage_metadata=None,
        )

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=fake_stream
        )
    )

    monkeypatch.setattr(
        gemini_service.genai,
        "Client",
        lambda **kwargs: fake_client,
    )

    chunks = list(
        gemini_service.stream_answer(
            "Explain brute force attacks",
            "T1110 - Brute Force",
        )
    )

    assert "T1110" in "".join(chunks)

    assert models_called == [
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
    ]
