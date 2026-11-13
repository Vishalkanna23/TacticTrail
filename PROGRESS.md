
# Progress

Commit after every class. Tag every Friday:
`git tag week-N && git push origin week-N`.

## Week 1 (tag week-1 by Fri 23 Oct)

- [ ] Repo created from the Examate template and registered on the form
- [ ] README top section filled from my project card
- [x] /health runs locally
- [ ] docs/QUESTIONS.md: 10 real questions
- [ ] 50+ pages collected, DATASET.md filled, sample in data/sample/
- [ ] Tag week-1 pushed

## Week 2 (tag week-2 by Fri 30 Oct)

- [x] POST /chat calls Gemini and returns structured JSON
- [x] Streaming, timeouts and fallback model implemented
- [x] Cost log + GET /usage verified locally
- [x] Docker Compose (API + PostgreSQL/pgvector) runs
- [x] GitHub Actions CI passed
- [x] Live deployment link documented in README
- [ ] Tag week-2 pushed

### Features completed

- [x] Gemini-powered RAG chat endpoint
- [x] Streaming Gemini responses
- [x] Gemini fallback and error handling
- [x] MITRE ATT&CK ID validation
- [x] Token usage and estimated cost tracking
- [x] PostgreSQL + pgvector integration
- [x] Imported 706 MITRE ATT&CK technique embeddings
- [x] Docker Compose integration for API and database

### Verification

- [x] 31 automated tests passed locally
- [x] Ruff checks passed
- [x] Dockerized API successfully queried PostgreSQL
- [x] GitHub Actions CI passed
- [x] Code pushed to GitHub

### Additional completed work

- [x] Keyword search
- [x] BM25 search
- [x] Semantic search using ONNX Runtime
- [x] Gemini AI explanations through /api/techniques/{technique_id}/explain
- [x] Docker deployment on Render

### GitHub

Week 2 implementation commit: `a727a03`

## Week 3 (tag week-3 by Fri 6 Nov)

- [ ] Parser keeps page numbers and headings
- [ ] 500+ pages chunked, embedded and stored in pgvector
- [ ] POST /ask answers with [document, page] citations
- [ ] docs/EVAL_v0.md with my 10 questions scored
- [ ] Tag week-3 pushed

## Daily log

| Date | What I did today | Commit |
|---|---|---|
| 2026-11-13 | Week 2 streaming validation, Docker integration and CI | a727a03 |
