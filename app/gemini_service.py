
import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_answer(question: str, evidence: str) -> str:
    """Generate an answer grounded in retrieved MITRE evidence."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are TacticTrail, a cybersecurity threat intelligence assistant.

Answer the analyst's question using ONLY the MITRE evidence below.

Rules:
- Never invent MITRE ATT&CK technique IDs.
- Use only technique IDs present in the evidence.
- Include the official MITRE source URL.
- If the evidence is insufficient, say so.

MITRE evidence:
{evidence}

Analyst question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    return response.text
