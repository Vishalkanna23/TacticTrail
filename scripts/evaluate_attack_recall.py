"""Evaluate MITRE ATT&CK technique retrieval against a human-labeled JSONL set.

Works against existing TacticTrail HTTP search endpoints or an offline predictions
JSONL file. Only Python standard-library dependencies are used. Retrieval metrics
are not a substitute for validating Gemini's generated answer claims or citations.
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ID_PATTERN = re.compile(r"^T\d{4}(?:\.\d{3})?$")
ENDPOINTS = {
    "keyword": ("/api/techniques/search", "keyword"),
    "bm25": ("/api/techniques/bm25", "query"),
    "semantic": ("/api/techniques/semantic", "query"),
    "pgvector": ("/api/techniques/pgvector", "query"),
}


def read_jsonl(path):
    """Load and validate nonempty JSONL dictionaries."""
    records = []
    with Path(path).open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            records.append(record)
    if not records:
        raise ValueError(f"{path}: no records")
    return records


def load_cases(path):
    cases = read_jsonl(path)
    seen = set()
    for case in cases:
        case_id = case.get("id")
        question = case.get("query")
        gold = case.get("gold_ids")
        abstain = case.get("abstain", False)
        if not isinstance(case_id, str) or not case_id.strip() or case_id in seen:
            raise ValueError("Each evaluation case requires a unique nonempty id")
        seen.add(case_id)
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"{case_id}: missing query")
        if not isinstance(gold, list) or any(
            not isinstance(value, str) or not ID_PATTERN.fullmatch(value)
            for value in gold
        ) or len(gold) != len(set(gold)):
            raise ValueError(f"{case_id}: gold_ids must be unique MITRE technique IDs")
        if not isinstance(abstain, bool) or (abstain and gold) or (not abstain and not gold):
            raise ValueError(f"{case_id}: give gold_ids or set abstain=true")
    return cases


def load_predictions(path):
    predictions = {}
    for record in read_jsonl(path):
        case_id, ids = record.get("id"), record.get("retrieved_ids")
        if not isinstance(case_id, str) or case_id in predictions:
            raise ValueError("Prediction IDs must be unique strings")
        if not isinstance(ids, list) or any(not isinstance(item, str) for item in ids):
            raise ValueError(f"{case_id}: retrieved_ids must be a list of strings")
        predictions[case_id] = ids
    return predictions


def fetch_retrieval(query, *, base_url, method, timeout=15):
    path, key = ENDPOINTS[method]
    url = f"{base_url.rstrip('/')}{path}?{urlencode({key: query})}"
    with urlopen(url, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ValueError("Search endpoint did not return a results list")
    return [item["technique_id"] for item in payload["results"]]


def load_known_ids(path):
    with Path(path).open(encoding="utf-8") as source:
        records = json.load(source)
    return {row["technique_id"] for row in records}


def unique_top_k(ids, k=3):
    unique = []
    for technique_id in ids:
        if technique_id not in unique:
            unique.append(technique_id)
        if len(unique) >= k:
            break
    return unique


def evaluate(cases, predictions, *, known_ids=None, k=3):
    """Strict Recall@k: every gold technique must appear among top-k results."""
    if not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    details = []
    answerable = correct = any_hit = abstained = correct_abstentions = 0
    unknown_returned = set()
    for case in cases:
        case_id = case["id"]
        if case_id not in predictions:
            raise ValueError(f"Missing predictions for {case_id}")
        raw_ids = predictions[case_id]
        if any(not isinstance(item, str) for item in raw_ids):
            raise ValueError(f"{case_id}: predictions must be strings")
        ranked = unique_top_k(raw_ids, k)
        bad_ids = [item for item in ranked if not ID_PATTERN.fullmatch(item)]
        if known_ids is not None:
            bad_ids.extend(item for item in ranked if item not in known_ids)
        unknown_returned.update(bad_ids)
        gold = set(case["gold_ids"])
        if case.get("abstain", False):
            abstained += 1
            success = not ranked
            correct_abstentions += success
        else:
            answerable += 1
            success = gold.issubset(set(ranked))
            correct += success
            any_hit += bool(gold.intersection(ranked))
        details.append({
            "id": case_id,
            "query": case["query"],
            "gold_ids": case["gold_ids"],
            "retrieved_ids": ranked,
            "passed": success,
            "abstain": case.get("abstain", False),
        })
    recall = correct / answerable if answerable else None
    return {
        "total_cases": len(cases),
        "answerable_cases": answerable,
        "strict_recall_at_3": recall if k == 3 else None,
        "strict_recall_at_k": recall,
        "any_hit_at_k": any_hit / answerable if answerable else None,
        "complete_gold_matches": correct,
        "abstention_cases": abstained,
        "correct_abstentions": correct_abstentions,
        "abstention_accuracy": (correct_abstentions / abstained) if abstained else None,
        "invalid_or_unknown_returned_ids": sorted(unknown_returned),
        "target_92_percent_met": (recall >= 0.92) if answerable >= 100 else None,
        "k": k,
        "cases": details,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--api-base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--method", choices=ENDPOINTS, default="semantic")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--known-techniques", type=Path,
                        default=Path("data/raw/enterprise_techniques.json"))
    parser.add_argument("--json-out", type=Path)
    arguments = parser.parse_args(argv)
    cases = load_cases(arguments.dataset)
    known_ids = (load_known_ids(arguments.known_techniques)
                 if arguments.known_techniques.exists() else None)
    if arguments.predictions:
        predictions = load_predictions(arguments.predictions)
    else:
        predictions = {
            case["id"]: fetch_retrieval(
                case["query"], base_url=arguments.api_base_url,
                method=arguments.method, timeout=arguments.timeout
            )
            for case in cases
        }
    report = evaluate(cases, predictions, known_ids=known_ids)
    summary = {key: value for key, value in report.items() if key != "cases"}
    print(json.dumps(summary, indent=2))
    if arguments.json_out:
        arguments.json_out.parent.mkdir(parents=True, exist_ok=True)
        arguments.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    main()
