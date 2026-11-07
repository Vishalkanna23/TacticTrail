import json
from datetime import UTC, datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "data" / "usage_log.jsonl"


def record_usage(model, input_tokens, output_tokens, total_tokens):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": estimate_cost(
        model, input_tokens, output_tokens
    ),
}

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")


def get_usage_totals():
    totals = {
        "api_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "estimated_cost_usd": 0.0,
    }

    if not LOG_FILE.exists():
        return totals

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            entry = json.loads(line)

            totals["api_calls"] += 1
            totals["input_tokens"] += entry["input_tokens"]
            totals["output_tokens"] += entry["output_tokens"]
            totals["total_tokens"] += entry["total_tokens"]

            cost = entry.get("estimated_cost_usd")

            if cost is None:
                    cost = estimate_cost(
                        entry["model"],
                        entry["input_tokens"],
                        entry["output_tokens"],
                    )

            if cost is not None:
                totals["estimated_cost_usd"] += cost

    totals["estimated_cost_usd"] = round(
        totals["estimated_cost_usd"], 8
    )

    return totals
def estimate_cost(model, input_tokens, output_tokens):
    rates = {
        "gemini-3.5-flash-lite": (0.30, 2.50),
        "gemini-3.1-flash-lite": (0.25, 1.50),
    }

    model = model.removeprefix("models/")

    for model_name, (input_rate, output_rate) in rates.items():
        if model.startswith(model_name):
            cost = (
                input_tokens * input_rate
                + output_tokens * output_rate
            ) / 1_000_000

            return round(cost, 8)

    return None