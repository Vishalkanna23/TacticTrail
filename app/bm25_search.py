
import json
import re

from rank_bm25 import BM25Okapi

from app import technique_search


def search_bm25(query):
    query_tokens = re.findall(r"\w+", query.lower())

    if not query_tokens:
        return []

    with open(technique_search.DATA_FILE, encoding="utf-8") as file:
        techniques = json.load(file)

    if not techniques:
        return []

    documents = []

    for technique in techniques:
        text = technique["name"] + " " + technique["description"]
        tokens = re.findall(r"\w+", text.lower())
        documents.append(tokens)

    bm25 = BM25Okapi(documents)

    scores = bm25.get_scores(query_tokens)

    results = []

    for technique, score in zip(techniques, scores, strict=True):
        if score > 0:
            results.append({
                **technique,
                "bm25_score": float(score)
            })

    results.sort(
        key=lambda technique: technique["bm25_score"],
        reverse=True
    )

    return results
