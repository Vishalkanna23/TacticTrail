# TacticTrail — Progress Tracker

## Progress Rules

Commit after every class.

Tag every Friday:

```bash
git tag week-N
git push origin week-N
```

---

## Week 1 — Project Setup
**Original deadline: Friday, 23 October 2026**

- [ ] Repo created from the Examate template and registered on the form
- [ ] README top section filled from my project card
- [x] `/health` endpoint runs locally
- [ ] `docs/QUESTIONS.md` contains 10 real questions
- [ ] 50+ pages collected, `DATASET.md` filled, sample in `data/sample/`
- [ ] Tag `week-1` pushed (not yet verified)

---

## Week 2 — Gemini RAG, Docker and Deployment
**Original deadline: Friday, 30 October 2026**

- [x] `POST /chat` calls Gemini and returns structured JSON
- [x] Streaming, timeouts and fallback model implemented
- [x] Cost log and `GET /usage` verified locally
- [x] Docker Compose (API + PostgreSQL/pgvector) runs
- [x] GitHub Actions CI passed
- [x] Live deployment link documented in README
- [x] Tag `week-2` pushed

### Features Completed

- [x] Gemini-powered RAG chat endpoint
- [x] Streaming Gemini responses
- [x] Gemini fallback and error handling
- [x] MITRE ATT&CK technique ID validation
- [x] Token usage and estimated cost tracking
- [x] PostgreSQL + pgvector integration
- [x] Imported 706 MITRE ATT&CK technique embeddings
- [x] Docker Compose integration for API and database

### Additional Features

- [x] Keyword search
- [x] BM25 search
- [x] Semantic search using ONNX Runtime
- [x] Gemini explanations through `/api/techniques/{technique_id}/explain`
- [x] Docker deployment on Render

### Verification

- [x] 31 automated tests passed at the original Week 2 checkpoint
- [x] Ruff checks passed
- [x] Dockerized API successfully queried PostgreSQL
- [x] GitHub Actions CI passed
- [x] Code pushed to GitHub

### GitHub

- Week 2 implementation commit: `a727a03`
- Week 2 tag: `week-2`
- Repository: https://github.com/Vishalkanna23/TacticTrail
- Deployment: https://tactictrail.onrender.com

**Week 2 status: Completed**

---

## Week 3 — PDF Ingestion, Document RAG and Evaluation
**Original deadline: Friday, 6 November 2026**

### Required Deliverables

- [x] Parser keeps page numbers and headings
- [ ] 500+ pages chunked, embedded and stored in pgvector
- [x] `POST /ask` answers with `[document, page]` citations
- [ ] `docs/EVAL_v0.md` with 10 questions scored
- [ ] Tag `week-3` pushed

### PDF Ingestion Pipeline

- [x] Installed PyMuPDF for PDF text extraction
- [x] Created `app/ingestion/pdf_parser.py`
- [x] Extracted text while preserving document page numbers
- [x] Implemented heuristic heading detection
- [x] Created `app/ingestion/chunker.py`
- [x] Implemented overlapping text chunks
- [x] Created `app/ingestion/embedder.py`
- [x] Generated embeddings using MiniLM ONNX
- [x] Implemented tokenizer truncation to prevent ONNX input-length errors
- [x] Created `app/ingestion/document_store.py`
- [x] Created PostgreSQL `document_chunks` table
- [x] Created `scripts/ingest_pdf.py`
- [x] Successfully ingested a real NIST cybersecurity PDF

### Document Ingestion Results

**Document:** NIST SP 800-61r3 — Incident Response Recommendations and Considerations for Cybersecurity Risk Management

- Source: NIST
- File: `NIST.SP.800-61r3.pdf`
- Imported chunks: **170**
- Embedding dimensions: **384**
- Embedding model: MiniLM ONNX
- Vector database: PostgreSQL + pgvector
- Metadata: Document name, page, heading and chunk ID
- Status: Ingestion successful

### Document Retrieval

- [x] Created `app/ingestion/document_search.py`
- [x] Implemented cosine similarity search using pgvector
- [x] Converted user questions into query embeddings
- [x] Retrieved the top matching document chunks
- [x] Returned source document, page number, heading, chunk ID and similarity score
- [x] Created `scripts/evaluate_document_search.py`
- [x] Tested retrieval using real cybersecurity questions

### Citation-Based RAG

- [x] Created `POST /ask` endpoint
- [x] Connected document retrieval with Gemini
- [x] Generated answers using retrieved PDF evidence
- [x] Included document-page citations in API responses
- [x] Added in-text citations to Gemini-generated answers
- [x] Created `app/ingestion/citation_validation.py`
- [x] Detected citations referencing pages outside retrieved evidence
- [x] Implemented safe fallback for missing or unverified citations
- [x] Added automated tests for citation validation
- [x] Successfully tested `/ask` against the NIST PDF

### Retrieval Evaluation

- [x] Created an initial three-question evaluation
- [x] Retrieved top three chunks for each question
- [x] Manually assessed retrieved chunks for relevance
- [x] Implemented Hit Rate@3 calculation
- [x] Completed the initial evaluation
- [ ] Expand evaluation to at least 10 varied cybersecurity questions
- [ ] Calculate Precision@3
- [ ] Document evaluation results in `docs/EVAL_v0.md`

### Initial Evaluation Results

**Document:** NIST SP 800-61r3

| Metric | Result |
|---|---|
| Questions evaluated | 3 |
| Retrieved chunks per question | 3 |
| Total chunks evaluated | 9 |
| Relevant chunks | 7 |
| Questions with at least one relevant chunk | 3 |
| Hit Rate@3 | **100%** |
| Manually labeled relevant chunks | **7/9 (77.78%)** |

**Questions evaluated:**

1. What does NIST recommend for cybersecurity incident response?
2. What should an incident response policy and plan include?
3. How should organizations prepare for cybersecurity incidents?

**Limitations:**

- Only three questions evaluated
- Only one document evaluated
- Relevance determined by manual labeling
- Similarity scores do not guarantee factual relevance
- Citation validation verifies retrieved document-page references but does not prove that every generated claim is supported
- Larger evaluations are needed before making strong accuracy claims

### Testing and Code Quality

- [x] PDF parser tests
- [x] Chunking tests
- [x] Embedding tests
- [x] Document storage tests
- [x] PDF ingestion pipeline tests
- [x] `/ask` endpoint tests
- [x] Citation validation tests
- [x] Missing-citation fallback tests
- [x] Ruff import-order issues resolved
- [x] Pytest and Ruff checks passed during Week 3

**Test count:** 42 tests explicitly confirmed passing in terminal output; additional test changes and successful checks followed. Verify the latest exact count with `python -m pytest -q`.

### Remaining Week 3 Work

- [ ] Prepare and ingest enough PDFs to reach 500+ pages
- [ ] Build a 10-question labeled evaluation dataset
- [ ] Calculate and document Hit Rate@3 and Precision@3
- [ ] Improve heading extraction and clean up extraction artifacts
- [ ] Improve citation and answer-grounding evaluation
- [ ] Create `docs/EVAL_v0.md`
- [ ] Update README with Week 3 features
- [ ] Commit and push Week 3 changes
- [ ] Create and push `week-3` Git tag

**Week 3 status: In progress — core PDF RAG implemented, remaining deliverables pending**

---

## Daily Log

| Date | What I did | Commit |
|---|---|---|
| 2026-11-13 | Week 2 streaming validation, Docker integration and CI | `a727a03` |
| 2026-11-14 | Week 3 PDF ingestion, semantic document search, citation-based RAG, tests and initial retrieval evaluation | Not yet recorded |

---

## GitHub Milestones

| Milestone | Status |
|---|---|
| Week 1 tag | Not verified |
| Week 2 tag | Completed and pushed |
| Week 3 tag | Pending |

---

## Next Milestone

**Complete the remaining Week 3 deliverables.**

1. Expand the evaluation from 3 to 10 questions.
2. Calculate retrieval quality metrics.
3. Complete `docs/EVAL_v0.md`.
4. Ingest at least 500 pages of source documents.
5. Run the full test suite and Ruff.
6. Update documentation, commit changes and push the `week-3` tag.
