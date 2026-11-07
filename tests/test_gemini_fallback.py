
from types import SimpleNamespace

from google.genai import errors

from app import gemini_service


def test_fallback_model(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    models_called = []

    def fake_generate_content(*, model, contents):
        models_called.append(model)

        if len(models_called) == 1:
            raise errors.ServerError(
                503,
                {"message": "Service unavailable"},
            )

        return SimpleNamespace(text="Fallback worked!")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=fake_generate_content
        )
    )

    monkeypatch.setattr(
        gemini_service.genai,
        "Client",
        lambda **kwargs: fake_client,
    )

    answer = gemini_service.generate_answer(
        "How do attackers steal passwords?",
        "T1110 - Brute Force",
    )

    assert answer == "Fallback worked!"

    assert models_called == [
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
    ]
