# Week 5 — ATT&CK retrieval evaluation harness

This is **evaluation infrastructure**, not a measured Week 5 success claim.

The starting questions in `docs/ATTACK_EVAL_SEED.jsonl` are adapted from
`docs/QUESTIONS.md`. The set contains **nine answerable hypothetical
scenarios and one abstention scenario**. It is **not** the planned 100-query
independent benchmark. Do not report Recall@3 >= 92% before testing at least
100 independent human-reviewed answerable questions.

## Run locally

From the project root with the API running:

```powershell
python scripts/evaluate_attack_recall.py --dataset docs/ATTACK_EVAL_SEED.jsonl --method semantic --json-out docs/week5_seed_results.json
```

Supported methods: `keyword`, `bm25`, `semantic`, `pgvector`. These
are the **existing separate endpoints**, not an implemented hybrid endpoint.
The evaluation does not use Gemini and does not require an AI API key.

You can also evaluate saved predictions offline:

```json
{"id":"Q01","retrieved_ids":["T1566.001","T1566.002","T1566"]}
```

Save one JSON record per line, then run:

```powershell
python scripts/evaluate_attack_recall.py --dataset docs/ATTACK_EVAL_SEED.jsonl --predictions predictions.jsonl
python -m pytest -q tests/test_attack_recall_eval.py
```

## Metrics

- **Strict Recall@3:** among answerable cases, the fraction where *every*
  gold technique ID occurs in the top three **unique** retrieved results.
- **Any Hit@3:** fraction of answerable cases with at least one gold ID in
  the top three. This is a diagnostic, not the strict primary metric.
- **Abstention accuracy:** separately counts cases where a query lacking
  matching ATT&CK evidence yielded no retrieved IDs. A retrieval endpoint
  is not an answer-generation abstention mechanism.
- **Invalid/unknown IDs:** flags retrieved strings not shaped like ATT&CK
  IDs or not present in the known local corpus, when that corpus is available.
  This is **not** a hallucination test on model-generated text.

The field `target_92_percent_met` remains null until at least 100
**answerable** cases are evaluated. Retrieval ranking scores do not measure
the truth of generated claims or NIST PDF citation accuracy.

## Still required to finish Week 5

1. Author and independently review 100+ gold-labeled ATT&CK queries.
2. Implement hybrid retrieval and re-ranking, and compare with baseline
   methods using the *same held-out cases*.
3. Test unsupported claims, fabricated technique IDs, forged citations,
   empty inputs, and fallback behavior with /chat and /ask.
4. Measure request latency (including p95), errors, usage, and costs with
   documented workloads and rate limits.
5. Re-run local tests and GitHub CI and document Demo Day 1 evidence.

Do not commit secrets, sample private incident data, or production credentials.
