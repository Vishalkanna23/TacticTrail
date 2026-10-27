
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.gemini_service import generate_answer
from app.technique_search import search_by_keyword, search_technique

app = FastAPI(title="TacticTrail", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


# FIRST: Keyword search
@app.get("/api/techniques/search")
def keyword_search(keyword: str):
    keyword = keyword.strip()

    if not keyword:
        raise HTTPException(
            status_code=400,
            detail="Keyword cannot be empty"
        )

    try:
        results = search_by_keyword(keyword)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Technique dataset is not available"
        ) from exc

    return {
        "keyword": keyword,
        "total_matches": len(results),
        "results": [
            {
                "technique_id": t["technique_id"],
                "name": t["name"],
                "url": t["url"]
            }
            for t in results[:10]
        ]
    }


# SECOND: Search using exact MITRE technique ID
@app.get("/api/techniques/{technique_id}")
def get_technique(technique_id: str):
    technique_id = technique_id.strip().upper()

    try:
        result = search_technique(technique_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Technique dataset is not available",
        ) from exc

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Technique ID not found"
        )

    return result


# THIRD: Explain technique using Gemini
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
