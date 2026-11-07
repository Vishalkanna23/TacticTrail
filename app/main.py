from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.bm25_search import search_bm25
from app.config import Settings, get_settings
from app.gemini_service import generate_answer
from app.semantic_search import search_semantic
from app.technique_search import search_by_keyword, search_technique
from app.usage_tracker import get_usage_totals

app = FastAPI(title="TacticTrail", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


class ChatRequest(BaseModel):
    question: str


# 1. Health check
@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up and running."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


# 2. Usage endpoint
@app.get("/usage")
def get_usage():
    return {
        "project": "TacticTrail",
        "description": "MITRE ATT&CK technique search and AI explanation API",
        "available_search_methods": [
            "keyword",
            "bm25",
            "semantic",
        ],
        "gemini_usage": get_usage_totals(),
    }


# 3. Keyword search
@app.get("/api/techniques/search")
def keyword_search(keyword: str):
    keyword = keyword.strip()

    if not keyword:
        raise HTTPException(
            status_code=400,
            detail="Keyword cannot be empty",
        )

    try:
        results = search_by_keyword(keyword)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Technique dataset is not available",
        ) from exc

    return {
        "keyword": keyword,
        "total_matches": len(results),
        "results": [
            {
                "technique_id": t["technique_id"],
                "name": t["name"],
                "url": t["url"],
                "relevance_score": t["relevance_score"],
            }
            for t in results[:10]
        ],
    }


# 4. BM25 search
@app.get("/api/techniques/bm25")
def bm25_search(query: str):
    query = query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty",
        )

    try:
        results = search_bm25(query)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Technique dataset is not available",
        ) from exc

    return {
        "query": query,
        "total_matches": len(results),
        "results": [
            {
                "technique_id": t["technique_id"],
                "name": t["name"],
                "url": t["url"],
                "bm25_score": t["bm25_score"],
            }
            for t in results[:10]
        ],
    }


# 5. Semantic search
@app.get("/api/techniques/semantic")
def semantic_search_endpoint(query: str):
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty",
        )

    results = search_semantic(query)

    return {
        "query": query,
        "total_matches": len(results),
        "results": [
            {
                "technique_id": technique["technique_id"],
                "name": technique["name"],
                "url": technique.get("url"),
                "similarity_score": technique["similarity_score"],
            }
            for technique in results
        ],
    }


# 6. Exact MITRE technique ID search
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
            detail="Technique ID not found",
        )

    return result


# 7. Explain technique using Gemini
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


# 8. Chat with Gemini using MITRE ATT&CK evidence
@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    # Find relevant MITRE techniques
    results = search_semantic(question, top_k=3)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant techniques found",
        )

    # Prepare evidence for Gemini
    evidence = "\n\n".join(
        f"ID: {technique['technique_id']}\n"
        f"Name: {technique['name']}\n"
        f"Description: {technique['description']}\n"
        f"Source: {technique['url']}"
        for technique in results
    )

    # Generate an evidence-grounded answer
    answer = generate_answer(
        question=question,
        evidence=evidence,
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "technique_id": technique["technique_id"],
                "name": technique["name"],
                "url": technique["url"],
            }
            for technique in results
        ],
    }
