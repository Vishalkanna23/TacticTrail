from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.gemini_service import generate_answer
from app.technique_search import search_technique

app = FastAPI(title="TacticTrail", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.get("/api/techniques/{technique_id}")
def get_technique(technique_id: str):
    # Normalize the technique ID
    technique_id = technique_id.strip().upper()

    # Search the MITRE dataset
    try:
        result = search_technique(technique_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Technique dataset is not available",
        ) from exc

    # Return 404 if the ID was not found
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Technique ID not found"
        )

    # Return the matching technique
    return result


@app.get("/api/techniques/{technique_id}/explain")
def explain_technique(technique_id: str):
    technique_id = technique_id.strip().upper()

    try:
        technique = search_technique(technique_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Technique dataset is not available",
        ) from exc

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail="Technique ID not found",
        )

    evidence = (
        f"ID: {technique['technique_id']}\n"
        f"Name: {technique['name']}\n"
        f"Description: {technique['description']}\n"
        f"Source: {technique['url']}"
    )

    answer = generate_answer(
        question=f"Explain MITRE technique {technique_id} in simple terms.",
        evidence=evidence,
    )

    return {
        "technique_id": technique["technique_id"],
        "name": technique["name"],
        "answer": answer,
        "source": technique["url"],
    }

