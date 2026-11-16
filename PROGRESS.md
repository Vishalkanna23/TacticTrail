# TacticTrail — Progress Tracker

**Last updated:** 16 November 2026
**Current phase:** Week 3 final documentation and release; Week 4 frontend is next
**Repository:** https://github.com/Vishalkanna23/TacticTrail

> This tracker separates *implemented and verified features* from *planned work*. Evaluation percentages below are based on the stated labeling method and must not be presented as proven answer accuracy.

## Progress Rules

Commit after every class or meaningful milestone. Tag a completed weekly milestone only after the deliverables have been verified:

```bash
git tag week-N
git push origin week-N
```

---

## Week 1 — Project Setup
**Original deadline: Friday, 23 October 2026**

- [ ] Repo creation from the Examate template and registration on the form — not independently verified
- [ ] README top section filled from the project card — original Week 1 checkpoint not independently verified
- [x] `/health` endpoint runs locally
- [x] `docs/QUESTIONS.md` contains 10 analyst questions (file verified; timing of original completion not verified)
- [ ] 50+ pages collected, `DATASET.md` filled, sample in `data/sample/` **by the original Week 1 deadline** — historical checkpoint not fully verified
- [ ] Tag `week-1` pushed — not verified

**Foundation now available:** FastAPI, the `/health` endpoint, the MITRE ATT&CK dataset register, a sample dataset, and 10 sample analyst questions. The historical Week 1 submission/tag remains unverified.

---

## Week 2 — Gemini RAG, Docker and Deployment
**Original deadline: Friday, 30 October 2026**

### Required Deliverables

- [x] `POST /chat` invokes Gemini and returns an answer and sources
- [x] Streaming, timeouts, and model fallback implemented
- [x] Cost log and `GET /usage` implemented and verified locally
- [x] Docker Compose (API + PostgreSQL/pgvector) runs
- [x] GitHub Actions CI passed at the Week 2 checkpoint
- [x] Live deployment documented
- [x] `week-2` tag pushed

### Features Completed

- [x] Ingested **706** active MITRE ATT&CK Enterprise techniques/sub-techniques
- [x] Exact technique ID lookup and basic keyword search
- [x] BM25 keyword-based ranking
- [x] Semantic search using ONNX Runtime and MiniLM embeddings
- [x] PostgreSQL + pgvector similarity search for technique embeddings
- [x] Gemini-assisted `/chat` and `/api/techniques/{technique_id}/explain`
- [x] `POST /chat/stream` streams responses to the client
- [x] Validation that generated MITRE technique IDs appear in retrieved evidence
- [x] Token-usage and estimated-cost tracking
- [x] Error handling, retry/fallback behavior, pytest, Ruff, and GitHub Actions CI
- [x] Docker Compose setup for FastAPI and PostgreSQL

### Verification and Links

- Week 2 checkpoint: **31 automated tests passed**
- Week 2 implementation commit: `a727a03`
- Tag: `week-2`
- Deployment recorded: https://tactictrail.onrender.com

**Week 2 status: Completed at its recorded checkpoint.**

---

## Week 3 — PDF Ingestion, Document RAG and Evaluation
**Original deadline: Friday, 6 November 2026**

### Required Deliverables

- [x] PDF parser preserves page numbers and detects heading candidates
- [x] **500+ PDF pages** chunked, embedded, and stored in pgvector — **540 distinct document pages verified**
- [x] `POST /ask` provides retrieved-document citations in `[document-name.pdf, page N]` format
- [x] `docs/EVAL_v0.md` generated with **10 scored questions** and documented AI-assessment limitations
- [ ] `week-3` Git tag pushed — **not yet done**

### 1. PDF Ingestion Pipeline

- [x] Added PyMuPDF-based parsing in `app/ingestion/pdf_parser.py`
- [x] Extracted text with original PDF page number and a heuristic heading candidate
- [x] Added `app/ingestion/chunker.py` with **800-character chunks** and **100-character overlap**
- [x] Added `app/ingestion/embedder.py` using the existing MiniLM ONNX model
- [x] Limited tokenizer input to **256 tokens** to prevent ONNX input-length issues
- [x] Generated **384-dimensional** embeddings
- [x] Added `app/ingestion/document_store.py` and parameterized PostgreSQL upsert
- [x] Added `scripts/create_document_chunks.sql` with `document_chunks` and `vector(384)`
- [x] Added command-line ingestion through `scripts/ingest_pdf.py`
- [x] Validated vector dimensions and finite embedding values before storage
- [x] Stored document name, PDF page, heading, per-document chunk ID, text, and embedding

### 2. Verified PDF Corpus

The following counts were confirmed by querying the live local PostgreSQL `document_chunks` table on **16 November 2026**:

| Source document | PDF pages represented in DB | Chunks in DB | Missing embeddings |
|---|---:|---:|---:|
| `NIST.SP.800-53r5.pdf` — Security and Privacy Controls for Information Systems and Organizations | 492 | 2,460 | 0 |
| `NIST.SP.800-61r3.pdf` — Incident Response Recommendations and Considerations for Cybersecurity Risk Management | 48 | 170 | 0 |
| **TOTAL** | **540** | **2,630** | **0** |

**Result:** The required 500-page ingestion threshold is met, with **40 pages above target**. These are **540 distinct pages with stored text chunks**, not merely 540 downloaded pages or 540 chunks. Local source PDFs remain untracked; do not add `data/documents/` to Git without reviewing size and redistribution terms.

### 3. Document Retrieval

- [x] Added `app/ingestion/document_search.py`
- [x] Embedded incoming questions using MiniLM ONNX
- [x] Queried pgvector using cosine distance (`embedding <=> query_embedding`)
- [x] Ranked nearest document chunks; returned document, page, heading, chunk ID, text, and similarity
- [x] Evaluated top-3 retrieved chunks with real cybersecurity questions

### 4. Citation-Based RAG (`POST /ask`)

- [x] Added `/ask` in `app/main.py`
- [x] Retrieved the top 3 relevant PDF **chunks**, not necessarily chunks from 3 different PDF files
- [x] Included retrieved passages and page metadata in Gemini's evidence prompt
- [x] Requested in-text document/page citations for factual paragraphs
- [x] Added `app/ingestion/citation_validation.py`
- [x] Rejected generated citations pointing to document/page pairs not in retrieved evidence
- [x] Used a safe fallback when no valid in-text citation appears or an unverified citation is found
- [x] Returned `citations` and `sources` lists with document/page metadata
- [x] Added tests covering valid citations, invented pages, missing citations, and empty questions

**Important limitation:** Citation validation checks that a **referenced document/page was retrieved**. It does **not** establish that each generated factual claim is actually supported by that page.

### 5. Retrieval Evaluation

#### Earlier manual baseline — 3 questions, one PDF

- [x] Created `scripts/evaluate_document_search.py` for manual `y/n` labeling
- [x] Measured Hit Rate@3 for the initial three-question NIST SP 800-61r3 evaluation

| Metric | Result |
|---|---:|
| Questions | 3 |
| Retrieved chunks | 9 |
| Manually labeled relevant chunks | 7 |
| Questions with at least one relevant chunk | 3 |
| Hit Rate@3 | **100.00%** |
| Share of chunks manually labeled relevant | **77.78% (7/9)** |

This initial sample is too small to establish general performance.

#### Current automated evaluation — 10 questions, two PDFs

- [x] Added `scripts/evaluate_document_search_ai.py` as a separate Gemini-based relevance evaluator
- [x] Preserved the manual evaluator for future comparisons
- [x] Retrieved up to **3 chunks per question** and asked Gemini to judge each independently
- [x] Calculated **Hit Rate@3** and **Precision@3** from the returned binary labels
- [x] Generated `docs/EVAL_v0.md` including per-question scores, source pages, AI reasons, and limitations
- [x] Inspected 3 selected full-text chunks against Gemini's judgments

**AI-assessed results (16 November 2026):**

| Metric | Result |
|---|---:|
| Questions evaluated | **10** |
| Retrieved chunks assessed | **30** |
| Chunks Gemini labeled relevant | **21/30** |
| Questions with at least one AI-relevant chunk | **10/10** |
| **AI-assessed Hit Rate@3** | **100.00%** |
| **AI-assessed Precision@3** | **70.00%** |

**Human spot-check (3 of 30 chunks):**

| Question / rank | Gemini label | Human review |
|---|---|---|
| Q2, rank 2 — incident response team responsibilities | Relevant | **Not sufficiently relevant**: introduces roles but does not explain the requested responsibilities |
| Q5, rank 1 — incident recovery considerations | Relevant | **Not sufficiently relevant**: mentions participants in recovery but not recovery considerations |
| Q9, rank 2 — managing user access permissions | Relevant | **Relevant**: addresses access-control policies and access rights |

If **only these two labels** are corrected, with all other AI labels unchanged, the **provisional mixed-label metrics** would be:

- **Hit Rate@3: 80.00% (8/10 questions)**
- **Precision@3: 63.33% (19/30 chunks)**

These adjusted percentages are **not fully human-verified metrics**. Retain both original AI-assessed and provisional adjusted scores in the report, and clearly label them. Gemini judgments can vary between runs.

### 6. Testing, CI, and Debugging

- [x] Local test suite: **43 passed** on 16 November 2026
- [x] Ruff checks passed on 16 November 2026
- [x] Tests cover PDF parsing, chunking, embeddings, ingestion, `/ask`, and citation validation
- [x] Resolved ONNX input-length error through tokenizer truncation
- [x] Resolved GitHub Actions failure caused by missing PyMuPDF in the dependency list
- [x] Added `pymupdf>=1.24` to `requirements.txt`
- [x] GitHub Actions CI passed for the dependency-fix commit (`a5baa8b`)
- [x] Week 3 PDF/RAG implementation progress committed as `b8129a7`
- [ ] New automated-evaluation files and updated documentation still need a final commit and CI verification

**Observed warning:** One non-blocking `google.genai` deprecation warning appears under local pytest. This does not affect the 43 passing tests.

### 7. Known Limitations and Future Improvements

- [ ] Improve heading detection; current font-size heuristic can select the wrong text
- [ ] Replace fixed-character splitting with sentence-aware chunking to avoid broken words/sentences
- [ ] Consider retrieval of more candidates, then re-ranking for precise relevance
- [ ] Strengthen the relevance rubric; mere topic mentions should not count as sufficient answers
- [ ] Conduct a full human-labeled evaluation rather than relying primarily on Gemini as judge
- [ ] Verify **claim-level** grounding, not only the document/page citation pattern
- [ ] Broaden the benchmark to more queries, documents, and edge cases
- [ ] Update README to reflect actual Week 3 implementation and results

### 8. Remaining Steps to Close Week 3

- [x] Ingest and verify at least 500 PDF pages
- [x] Produce a 10-question AI-scored evaluation report
- [x] Perform and document an initial human spot-check
- [x] Run local pytest and Ruff checks
- [ ] Review the final report's Markdown formatting in VS Code
- [ ] Update the README with Week 3 features and limitations
- [ ] Stage **only intended** Week 3 files (`PROGRESS.md`, `docs/EVAL_v0.md`, `scripts/evaluate_document_search_ai.py`, and any deliberately updated README)
- [ ] Commit, push, and confirm the latest GitHub Actions CI result
- [ ] Create and push the `week-3` Git tag

**Week 3 status: Core technical and evaluation deliverables completed; release/documentation/tag still pending.**

---

## Daily Log

| Date | What I did | Commit / verification |
|---|---|---|
| 2026-11-13 | Week 2 streaming validation, Docker integration, CI | `a727a03`; `week-2` tag recorded |
| 2026-11-14 | Week 3 PDF ingestion, semantic document search, citation-based RAG, initial retrieval evaluation | `b8129a7` |
| 2026-11-14 | Fixed CI dependency error by adding PyMuPDF | `a5baa8b`; GitHub Actions success |
| 2026-11-16 | Ingested NIST SP 800-53r5, verified **540 pages / 2,630 chunks / 0 missing embeddings** | Local PostgreSQL verification; not yet committed |
| 2026-11-16 | Completed 10-question Gemini evaluation and three-chunk human spot-check | `docs/EVAL_v0.md` created locally; not yet committed |
| 2026-11-16 | Confirmed **43 local tests passed** and Ruff passed | Local verification; new files still need CI |

---

## GitHub Milestones

| Milestone | Status |
|---|---|
| Week 1 tag | Not verified |
| Week 2 tag | Completed and pushed |
| Week 3 implementation progress commit (`b8129a7`) | Completed and pushed |
| Week 3 dependency-fix commit (`a5baa8b`) | Completed; CI passed |
| Week 3 final evaluation/report commit | Pending |
| Week 3 tag | Pending |

---

## Next Milestone — Week 4 Frontend

**Begin after the Week 3 final documentation, CI and tag are complete.**

Planned frontend direction (not yet implemented):

1. Set up React + Vite + Tailwind CSS.
2. Build a responsive TacticTrail dashboard.
3. Add MITRE ATT&CK technique search and result details.
4. Connect Gemini chat and the `/ask` PDF evidence experience.
5. Display verified source links, document-page citations, loading/error states, and streaming output.
6. Integrate the frontend with the FastAPI backend and test deployment.

**No frontend features should be marked completed until built and tested.**
