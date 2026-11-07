import json

from app import usage_tracker


def test_usage_totals_with_cost(tmp_path, monkeypatch):
    log_file = tmp_path / "usage_log.jsonl"
    monkeypatch.setattr(usage_tracker, "LOG_FILE", log_file)

    entry = {
        "model": "gemini-3.5-flash-lite",
        "input_tokens": 1000,
        "output_tokens": 100,
        "total_tokens": 1100,
    }

    log_file.write_text(json.dumps(entry) + "\n", encoding="utf-8")

    totals = usage_tracker.get_usage_totals()

    assert totals["api_calls"] == 1
    assert totals["input_tokens"] == 1000
    assert totals["output_tokens"] == 100
    assert totals["total_tokens"] == 1100
    assert totals["estimated_cost_usd"] == 0.00055