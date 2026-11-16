# TacticTrail

**Project ID:** B-ENT-05
**Status:** Week 3 implementation complete; final Git release pending (16 November 2026)
**Repository:** https://github.com/Vishalkanna23/TacticTrail

> An ID-safe threat-intelligence desk that maps observed attacker behavior to verified MITRE ATT&CK techniques, detections, and mitigations.

## Problem

Security operations center (SOC) analysts often need to turn incident notes into accurate MITRE ATT&CK technique mappings. Similar technique names and sub-technique IDs can be easy to confuse, while general-purpose AI systems may return plausible but incorrect identifiers. Analysts also spend time searching separate sources for related detections and mitigations. TacticTrail aims to make those investigations faster and more reliable by combining exact technique-ID matching with evidence-grounded AI answers.

## Who it is for

The intended user is a **threat-intelligence analyst or SOC analyst at a Bengaluru bank**, working with separate **retail-banking and corporate-banking** units. These are project personas, not a claim of a real bank deployment. Each unit is modeled as a separate tenant: analysts may consult shared public ATT&CK knowledge but must only access their own unit's private incident notes and alerts.

## Proposed solution

TacticTrail is being developed to let analysts:

- Search for a technique using its exact ATT&CK ID, name, or a natural-language incident description.
- See the verified **technique ID, technique name, tactic, official ATT&CK link, and supporting evidence**.
- Find relevant ATT&CK mitigations and detection guidance, where available.
- Compare closely related techniques without mixing up their identifiers.
- Later, ask an AI agent questions about authorized sample alert records, such as which techniques appeared most frequently during a month.

## Signature feature: ID-safe answers

Every technique-related answer must be checked against ingested MITRE ATT&CK records and include a valid technique ID, associated tactic, and source link. The system must **not invent a technique ID**. If the evidence is insufficient, it should say so rather than guess. A retrieved candidate is not automatically a confirmed incident attribution.

## Hardest problem (my interview story)

**Exact-term hybrid search with re-ranking.** Semantic search alone can retrieve a related but wrong technique when IDs or sub-technique names look similar. The system already provides separate search methods; combining and re-ranking them is future work:

1. **Exact-ID lookup** for ATT&CK identifiers, with strict validation (implemented).
2. **BM25 keyword search** for technique names and technical terms (implemented).
3. **Vector similarity search** for natural-language descriptions (implemented).
4. **Hybrid re-ranking** to prioritize evidence across the search methods (planned).

A planned later benchmark will use **100 representative analyst queries**. The goal is to have the correct technique ID in the **top three results for at least 92 of 100 queries (Recall@3 >= 92%)**, with **zero invented technique IDs** in the generated answers. Retrieval accuracy and final-answer correctness will be measured separately.

## Dataset

**MITRE ATT&CK source:** [MITRE ATT&CK](https://attack.mitre.org/) using the official [STIX 2.1 data repository](https://github.com/mitre-attack/attack-stix-data).

**Current technique index:** Enterprise ATT&CK v20.0, with **706 active techniques and sub-techniques** indexed using 384-dimensional embeddings.

**Current document knowledge base:**

| Document | Indexed PDF pages | Stored chunks |
|---|---:|---:|
| NIST SP 800-53 Rev. 5 — Security and Privacy Controls for Information Systems and Organizations | 492 | 2,460 |
| NIST SP 800-61 Rev. 3 — Incident Response Recommendations and Considerations for Cybersecurity Risk Management | 48 | 170 |
| **Total** | **540** | **2,630** |

All 2,630 stored document chunks were confirmed to have embeddings in the local PostgreSQL database on 16 November 2026. The technique records and NIST document chunks are distinct datasets.

See [DATASET.md](DATASET.md) for dataset provenance and collection details. Mobile/ICS ATT&CK coverage, additional relationships, and tenant-scoped sample incident data are potential later extensions, not current verified capabilities.

## Example analyst questions

1. What is **T1566.002**, and how does it differ from **T1566.001**?
2. Which mitigations are relevant to credential dumping from **LSASS**?
3. Which known threat groups have used scheduled tasks for persistence?
4. In the sample alerts for my business unit, which ATT&CK techniques occurred most often this month? *(Planned agent feature.)*

See [docs/QUESTIONS.md](docs/QUESTIONS.md) for the analyst-question set. The **10 PDF retrieval evaluation questions** and their scores are recorded separately in [docs/EVAL_v0.md](docs/EVAL_v0.md).

## Technology and architecture

### Implemented

- **Backend:** Python and FastAPI.
- **Threat-intelligence dataset:** MITRE ATT&CK Enterprise v20.0 (706 active techniques/sub-techniques).
- **Document knowledge base:** NIST SP 800-53r5 and SP 800-61r3 PDFs.
- **Database:** PostgreSQL and pgvector for vector search.
- **Retrieval:** Exact ATT&CK ID lookup, keyword search, BM25, MiniLM semantic search, and pgvector similarity search.
- **Embeddings:** MiniLM using ONNX Runtime; 384-dimensional vectors.
- **AI integration:** Google Gemini for retrieval-assisted answers and explanation endpoints, including streaming and fallback handling.
- **Document RAG:** PyMuPDF parsing, overlapping text chunks, vector retrieval, `/ask` responses with document-page citations, and citation-format validation.
- **Engineering:** Docker Compose, pytest, Ruff, GitHub Actions CI, and a recorded Render deployment.

### Planned

- Hybrid ranking that combines the separate search methods and re-ranks candidates.
- Sentence-aware document chunking and stronger claim-level citation verification.
- React frontend and cybersecurity dashboard.
- User authentication and database-enforced tenant isolation.
- Read-only AI agent with authorized access to sample incident data.

### Current document question-answering flow

1. Receive a question at `POST /ask`.
2. Convert the question to a MiniLM embedding.
3. Retrieve the top three matching document chunks from PostgreSQL/pgvector.
4. Ask Gemini to answer using the retrieved passages and document-page references.
5. Validate that cited document/page pairs occur in the retrieved evidence.
6. Return the answer and source metadata, or a fallback when citations are invalid or missing.

**Important limitation:** Citation validation confirms that a cited document/page was retrieved; it does **not** prove that every answer claim is supported by that page.

## Security and reliability requirements

- Enforce tenant isolation in application and database access controls, not just through LLM prompts.
- Use a **read-only database role**, approved tables, row limits, query timeouts, and input validation for any generated SQL.
- Never execute LLM-produced write queries against alerts or user data.
- Show citations and clearly distinguish documented evidence from inference.
- Refuse to fabricate ATT&CK identifiers or unsupported evidence.
- Keep secrets in environment variables or local untracked files; never commit real API keys or incident secrets.

## Development roadmap

| Phase | Weeks | Planned deliverable |
|---|---|---|
| Foundation | 1–2 | README, questions, initial dataset, running API, LLM endpoint, CI and live deployment |
| RAG retrieval | 3–4 | Data ingestion, citations, hybrid search, background jobs and tenant login |
| Evaluation and demo | 5–6 | Recall@3 tests, safety checks, load/cost measurement, Demo Day 1 |
| AI agent | 7–9 | Agent using TacticTrail, tools/MCP, memory, planning and human approval |
| Hardening and final demo | 10–12 | Agent tests, safe background jobs, cost controls and final demonstration |

**Demo Day 1:** 28 November 2026
**Final Demo Day:** 9 January 2027

See [PROGRESS.md](PROGRESS.md) for the repository's detailed weekly checklist. A planned milestone is **not** a completed feature.

## Current implementation status

TacticTrail has completed the Week 2 backend foundation and the core Week 3 PDF ingestion, document retrieval, and citation-based question-answering work. Week 3 release/tagging is still pending.

### Verified Week 3 results

| Measure | Result |
|---|---:|
| NIST PDFs indexed | 2 |
| Distinct document pages represented | 540 |
| Stored document chunks | 2,630 |
| Chunks missing embeddings | 0 |
| Retrieval evaluation questions | 10 |
| AI-assessed Hit Rate@3 | 100.00% (10/10 questions) |
| AI-assessed Precision@3 | 70.00% (21/30 chunks) |
| Provisional adjusted Hit Rate@3 | 80.00% (8/10 questions) |
| Provisional adjusted Precision@3 | 63.33% (19/30 chunks) |
| Automated tests | 43 passed |

The provisional adjusted metrics correct **two** AI judgments after manually inspecting **three** chunks, while leaving the other 28 AI labels unchanged. They are **not** a fully human-labeled benchmark. The metrics evaluate **retrieval**, not factual correctness of generated answers.

The local verification also passed `python -m ruff check .`; pytest reported one non-blocking third-party deprecation warning. Detailed methodology and limitations are in [docs/EVAL_v0.md](docs/EVAL_v0.md).

### Remaining work

- Commit final Week 3 documentation and evaluation files; push the `week-3` Git tag.
- Build the React frontend in Week 4.
- Improve chunk boundaries, relevance judging, retrieval ranking, and citation grounding.
- Implement authentication, tenant isolation, and later AI agent features.

## Run TacticTrail locally

### Windows PowerShell (VS Code terminal)

Requires Python and Git. From the parent folder where you want the project:

```powershell
git clone https://github.com/Vishalkanna23/TacticTrail.git
cd TacticTrail
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

If you already cloned the repository, skip `git clone` and open your existing `TacticTrail` folder. In a browser, visit **http://127.0.0.1:8000/health**. This endpoint checks backend health. API routes are documented at **http://127.0.0.1:8000/docs**; database- and Gemini-backed features also require their corresponding services and environment configuration.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Live link

Backend deployment recorded during Week 2: https://tactictrail.onrender.com

The deployed service may not yet include all locally implemented Week 3 features.

## MITRE ATT&CK attribution and terms

TacticTrail is a student project and is **not affiliated with or endorsed by MITRE**. ATT&CK® is a registered trademark of The MITRE Corporation. Review the [MITRE ATT&CK Terms of Use](https://attack.mitre.org/resources/legal-and-branding/terms-of-use/) before downloading or redistributing its data, and reproduce the applicable MITRE copyright designation and license with any redistributed copies.

> © 2026 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.


## Week 2 — RAG Chat and PostgreSQL Integration

The Week 2 checkpoint established the backend foundation used by the Week 3 document-RAG work.

### Features implemented

- MITRE ATT&CK technique search using keywords and BM25.
- Semantic search using MiniLM ONNX embeddings.
- PostgreSQL + pgvector similarity search.
- 706 active MITRE ATT&CK techniques/sub-techniques stored with embeddings.
- Gemini-assisted cybersecurity question answering.
- Streaming responses, model fallback, and error handling.
- MITRE technique ID validation against retrieved evidence.
- Gemini token usage and estimated cost tracking.
- Docker Compose integration for FastAPI and PostgreSQL.
- Automated testing with pytest and Ruff; GitHub Actions CI.

### Run with Docker Compose

Configure the local `.env` file with the necessary non-committed settings, start Docker Desktop, then run:

```powershell
docker compose up -d --build
```

Open the API documentation at http://localhost:8000/docs.

### Important endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Application health |
| `GET /usage` | Gemini usage statistics |
| `GET /api/techniques/search` | Keyword-based technique search |
| `GET /api/techniques/bm25` | BM25 technique search |
| `GET /api/techniques/semantic` | Semantic technique search |
| `GET /api/techniques/pgvector` | PostgreSQL vector similarity search |
| `GET /api/techniques/{technique_id}/explain` | Gemini-assisted technique explanation |
| `POST /chat` | Retrieval-assisted Gemini chat |
| `POST /chat/stream` | Streaming Gemini responses |
| `POST /ask` | Week 3 document question-answering with citations |

### Testing

```powershell
python -m pytest -q
python -m ruff check .
```

The recorded Week 2 checkpoint had **31 passing tests** and successful GitHub Actions CI. The later local Week 3 verification had **43 passing tests**.
