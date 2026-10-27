
from app.gemini_service import generate_answer
from app.technique_search import search_technique

technique = search_technique("T1566.001")

if technique is None:
    print("Technique not found in local MITRE dataset.")
else:
    question = "Explain MITRE technique T1566.001 in simple terms."

    evidence = (
        f"ID: {technique['technique_id']}\n"
        f"Name: {technique['name']}\n"
        f"Description: {technique['description']}\n"
        f"Source: {technique['url']}"
    )

    answer = generate_answer(question, evidence)

    print("\nGemini's answer:\n")
    print(answer)
