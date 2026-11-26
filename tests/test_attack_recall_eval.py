"""Offline tests for evaluation math; these make no model/network/database calls."""

import json

import pytest

from scripts.evaluate_attack_recall import evaluate, load_cases, load_predictions


def case(case_id, gold=None, abstain=False):
    return {
        "id": case_id, "query": f"Query {case_id}",
        "gold_ids": gold or [], "abstain": abstain,
    }


def test_strict_recall_requires_all_gold_ids_in_top_three():
    cases = [case("one", ["T1566.001", "T1566.002"]),
             case("two", ["T1486"])]
    predictions = {"one": ["T1566.001", "T1003", "T1078"],
                   "two": ["T1486", "T1486", "T1078"]}
    report = evaluate(cases, predictions, known_ids={
        "T1566.001", "T1566.002", "T1003", "T1078", "T1486"
    })
    assert report["strict_recall_at_3"] == 0.5
    assert report["any_hit_at_k"] == 1.0
    assert report["target_92_percent_met"] is None
    assert report["cases"][1]["retrieved_ids"] == ["T1486", "T1078"]


def test_abstention_measured_separately():
    report = evaluate([case("x", ["T1486"]), case("y", abstain=True)],
                      {"x": ["T1486"], "y": []})
    assert report["answerable_cases"] == 1
    assert report["strict_recall_at_3"] == 1.0
    assert report["abstention_accuracy"] == 1.0


def test_unknown_ids_reported_without_counting_them_as_evidence():
    report = evaluate([case("one", ["T1486"])],
                      {"one": ["T9999", "fake", "T1486"]},
                      known_ids={"T1486"})
    assert report["invalid_or_unknown_returned_ids"] == ["T9999", "fake"]


def test_input_validation_and_duplicates(tmp_path):
    dataset = tmp_path / "cases.jsonl"
    dataset.write_text(json.dumps(case("x", ["T1486"])) + "\n" +
                       json.dumps(case("x", ["T1078"])) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        load_cases(dataset)
    dataset.write_text(json.dumps(case("x", ["T1486"])) + "\n", encoding="utf-8")
    assert len(load_cases(dataset)) == 1
    preds = tmp_path / "pred.jsonl"
    preds.write_text('{"id":"x","retrieved_ids":["T1486"]}\n', encoding="utf-8")
    assert load_predictions(preds) == {"x": ["T1486"]}


def test_missing_prediction_fails_explicitly():
    with pytest.raises(ValueError, match="Missing predictions"):
        evaluate([case("x", ["T1486"])], {})
