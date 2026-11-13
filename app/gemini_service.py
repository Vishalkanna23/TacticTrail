import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from app.usage_tracker import record_usage

load_dotenv()


def generate_answer(question: str, evidence: str) -> str:
    """Generate an answer grounded in retrieved MITRE evidence."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30000,
            retry_options=types.HttpRetryOptions(
                attempts=3,
                initial_delay=1.0,
                max_delay=4.0,
            ),
        ),
    )

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

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
    except errors.APIError as error:
        if error.code not in (429, 500, 502, 503, 504):
            raise

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    usage = getattr(response, "usage_metadata", None)

    if usage:
        input_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        total_tokens = usage.total_token_count or 0

        record_usage(
            model=getattr(response, "model_version", None) or "unknown",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )

        print("Input tokens:", input_tokens)
        print("Output tokens:", output_tokens)
        print("Total tokens:", total_tokens)

    return response.text

def stream_answer(question: str, evidence: str):
    """Stream an answer grounded in MITRE evidence."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=30000),
    )

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

    models = (
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
    )

    for model in models:
        emitted_text = False
        last_usage = None

        try:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=prompt,
            ):
                usage = getattr(chunk, "usage_metadata", None)

                if usage is not None:
                    last_usage = usage

                if chunk.text:
                    emitted_text = True
                    yield chunk.text

            if not emitted_text:
                raise RuntimeError("Gemini returned an empty stream")

            if last_usage:
                record_usage(
                    model=model,
                    input_tokens=last_usage.prompt_token_count or 0,
                    output_tokens=last_usage.candidates_token_count or 0,
                    total_tokens=last_usage.total_token_count or 0,
                )

            return
        except errors.APIError as error:
            if emitted_text:
                yield (
                    "\n\n[TacticTrail Warning: Gemini stopped responding "
                    "before completing the answer. "
                    "The response above is incomplete. Please retry.]"
                )
                return

            if error.code not in (429, 500, 502, 503, 504):
                raise

            if model == models[-1]:
                yield (
                    "\n\n[TacticTrail Error: Both Gemini models "
                    "are currently unavailable. Please try again later.]"
                )
                return
