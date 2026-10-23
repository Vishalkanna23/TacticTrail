# TacticTrail

**Project ID:** B-ENT-05  
**Status:** Week 1 — starter application; core search and AI features are planned  
**Repository:** https://github.com/Vishalkanna23/TacticTrail

> An ID-safe threat-intelligence desk that maps observed attacker behavior to verified MITRE ATT&CK techniques, detections, and mitigations.

## Problem

Security operations center (SOC) analysts often need to turn incident notes into accurate MITRE ATT&CK technique mappings. Similar technique names and sub-technique IDs can be easy to confuse, while general-purpose AI systems may return plausible but incorrect identifiers. Analysts also spend time searching separate sources for related detections and mitigations. TacticTrail aims to make those investigations faster and more reliable by combining exact technique-ID matching with evidence-grounded AI answers.

## Who it is for

The intended user is a **threat-intelligence analyst or SOC analyst at a Bengaluru bank**, working with separate **retail-banking and corporate-banking** units. These are project personas, not a claim of a real bank deployment. Each unit is modeled as a separate tenant: analysts may consult shared public ATT&CK knowledge but must only access their own unit's private incident notes and alerts.

## Proposed solution

TacticTrail will let analysts:

- Search for a technique using its exact ATT&CK ID, name, or a natural-language incident description.
- See the verified **technique ID, technique name, tactic, official ATT&CK link, and supporting evidence**.
- Find relevant ATT&CK mitigations and detection guidance, where available.
- Compare closely related techniques without mixing up their identifiers.
- Later, ask an AI agent questions about authorized sample alert records, such as which techniques appeared most frequently during a month.

## Signature feature: ID-safe answers

Every technique-related answer must be checked against ingested MITRE ATT&CK records and include a valid technique ID, associated tactic, and source link. The system must **not invent a technique ID**. If the evidence is insufficient, it should say so rather than guess. A retrieved candidate is not automatically a confirmed incident attribution.

## Hardest problem (my interview story)

**Exact-term hybrid search with re-ranking.** Semantic search alone can retrieve a related but wrong technique when IDs or sub-technique names look similar. The planned retrieval system combines:

1. **Exact-ID lookup** for ATT&CK identifiers, with strict validation.
2. **BM25 keyword search** for technique names, group names, and technical terms.
3. **Vector similarity search** for natural-language descriptions.
4. **Re-ranking and verification** to prioritize the correct evidence before generating a cited answer.

The system will be tested using **100 representative analyst queries**. The goal is to have the correct technique ID in the **top three results for at least 92 of 100 queries (Recall@3 >= 92%)**, with **zero invented technique IDs** in the generated answers. Retrieval accuracy and final-answer correctness will be measured separately.

## Dataset

**Authoritative source:** [MITRE ATT&CK](https://attack.mitre.org/), using the official [STIX 2.1 dataset repository](https://github.com/mitre-attack/attack-stix-data).

| Source | Link | Documents / records | Pages / page equivalents | Licence / terms |
|---|---|---|---|---|
| MITRE ATT&CK — Enterprise, Mobile and ICS | [Official STIX data](https://github.com/mitre-attack/attack-stix-data) | Target: 1,500+ technique, group and software records/pages | Target: 2,000+ page equivalents; conversion method to be documented | [MITRE ATT&CK Terms of Use](https://attack.mitre.org/resources/legal-and-branding/terms-of-use/) |

**Current ingestion:** Not yet recorded or verified. Actual downloaded file counts, record counts, ATT&CK version, download date, and the page-equivalent calculation will be documented in [DATASET.md](DATASET.md). Week 1 aims to collect the first 50+ page equivalents; Week 3 aims to ingest at least 500.

The dataset will include techniques and sub-techniques, groups, software, mitigations, and relevant ATT&CK relationships. Public ATT&CK data and private, tenant-scoped sample incidents will be stored and accessed separately.

## Example analyst questions

1. What is **T1566.002**, and how does it differ from **T1566.001**?
2. Which mitigations are relevant to credential dumping from **LSASS**?
3. Which known threat groups have used scheduled tasks for persistence?
4. In the sample alerts for my business unit, which ATT&CK techniques occurred most often this month? *(Planned agent feature.)*

The full set of **10 evaluation questions** will be maintained in [docs/QUESTIONS.md](docs/QUESTIONS.md) as a separate Week 1 deliverable.

## Planned technology and architecture

- **Backend:** Python and FastAPI (starter already present).
- **Threat-intelligence data:** Official MITRE ATT&CK STIX 2.1 JSON.
- **Structured storage:** PostgreSQL (planned).
- **Retrieval:** exact-ID lookup, BM25, vector search/pgvector, and re-ranking (planned).
- **Answering:** an LLM grounded in retrieved ATT&CK evidence, with citations (planned).
- **Agent:** read-only, tenant-authorized SQL queries over sample alert data, plus TacticTrail retrieval tools (Weeks 7–12).
- **Engineering:** automated tests, GitHub Actions, Docker and a deployed demo (to be validated or built as milestones progress).

**Planned answer flow:** Analyst question -> validated tenant context -> exact-ID / BM25 / vector retrieval -> re-ranking -> ATT&CK ID verification -> cited answer.

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

The repository currently contains a **FastAPI starter** with a `GET /health` endpoint, dependency files, tests and workflow scaffolding. The RAG index, hybrid retrieval, authentication, full dataset ingestion, and AI agent are **not yet confirmed as implemented**. This section will be updated when features are built and tested.

## Run the starter locally

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

If you already cloned the repository, skip `git clone` and open your existing `TacticTrail` folder. In a browser, visit **http://127.0.0.1:8000/health**. This endpoint is a startup health check; it is **not** a working AI search endpoint.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Live link

**Not deployed yet.** A verified deployment URL will be added as part of the Week 2 milestone.

## MITRE ATT&CK attribution and terms

TacticTrail is a student project and is **not affiliated with or endorsed by MITRE**. ATT&CK® is a registered trademark of The MITRE Corporation. Review the [MITRE ATT&CK Terms of Use](https://attack.mitre.org/resources/legal-and-branding/terms-of-use/) before downloading or redistributing its data, and reproduce the applicable MITRE copyright designation and license with any redistributed copies.

> © 2026 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.
