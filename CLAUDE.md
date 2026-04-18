# SMB AI Business Assistant — CLAUDE.md

## Project Purpose

An AI-powered business intelligence assistant for local Indian SMBs (restaurants, retail shops, clinics, coaching centers). Business owners upload their data (sales CSVs, customer feedback, invoices, WhatsApp exports) and get an AI assistant that answers business questions, identifies revenue patterns, and suggests actions.

**Primary goal: Learning to get hired as an AI engineer.** The user is building this project to deeply understand every layer of a production RAG system, not just to ship it. Every design decision should be explainable in an interview. The learning comes first; the build is the vehicle.

---

## System Architecture (Build Target)

```
User uploads CSVs / PDFs / text
            ↓
    FastAPI backend
            ↓
   Ingestion pipeline (chunking + cleaning)
            ↓
  Hybrid retrieval (BM25 + dense vectors)
  ChromaDB + MiniLM-L6-v2
            ↓
   Query rewriting + re-ranking
            ↓
  LLM generation (Anthropic Claude API)
            ↓
  Structured output + Pydantic validation
            ↓
  RAGAS eval pipeline + LangSmith tracing
            ↓
  Gradio frontend on Hugging Face Spaces
```

---

## 4-Week Roadmap

### Week 1 — Foundation + Ingestion Pipeline (Topics: Python, Embeddings)
- [x] Day 1–2: Pydantic models (`DocumentChunk`, `BusinessDocument`) — DONE
- [ ] Day 3–4: `DocumentLoader` (CSV, PDF, TXT) + `SemanticChunker` with overlap
- [ ] Day 5–6: `VectorStore` wrapper (ChromaDB + MiniLM embeddings)
- [ ] Day 7: `docs/week1.md` — decisions + architecture diagram

### Week 2 — Retrieval Layer + FastAPI Backend (Topics: RAG, Prompt Engineering, LLM APIs)
- [ ] Day 8–9: `BM25Retriever` + `HybridRetriever` with RRF fusion
- [ ] Day 10–11: `QueryRewriter` + system prompt design
- [ ] Day 12–13: Full FastAPI backend (`/health`, `/upload`, `/query`, `/query/stream`)
- [ ] Day 14: `docs/week2.md`

### Week 3 — Evaluation + Observability + Agents (Topics: Evaluation, Fine-tuning concepts, Agents)
- [ ] Day 15–16: RAGAS evaluation pipeline + golden QA dataset (20 pairs)
- [ ] Day 17–18: LangSmith tracing + structured logging
- [ ] Day 19–20: Agentic layer with tool calling (`search_business_data`, `calculate_metric`)
- [ ] Day 21: `docs/week3.md` — actual RAGAS scores + LangSmith screenshots

### Week 4 — Frontend + Deployment + Polish (Topics: Deployment, System Design, Databases)
- [ ] Day 22–23: Gradio frontend connected to FastAPI
- [ ] Day 24–25: Docker + docker-compose + HF Spaces deploy
- [ ] Day 26–27: README with architecture diagram + LinkedIn post draft
- [ ] Day 28: Final RAGAS eval run, record demo video, publish

---

## Topic-to-Code Mapping

| Topic | Where it shows up in this codebase |
|---|---|
| Python essentials (Pydantic, async, type hints) | `backend/ingestion/models.py`, everywhere |
| Linear algebra basics | `backend/retrieval/vector_store.py` — cosine similarity |
| Transformer architecture | Background knowledge for explaining MiniLM |
| Embeddings & vector search | `backend/retrieval/vector_store.py` |
| RAG | `backend/retrieval/hybrid_retriever.py` |
| Prompt engineering | `backend/retrieval/query_rewriter.py`, system prompt |
| Fine-tuning concepts | Understanding why RAG > fine-tuning for this use case |
| Agentic systems | `backend/agents/business_analyst.py` |
| LLM APIs | Anthropic SDK usage throughout generation layer |
| Evaluation & monitoring | `backend/evaluation/ragas_eval.py` |
| Deployment | `Dockerfile`, `docker-compose.yml`, HF Spaces |
| Databases | ChromaDB (`backend/retrieval/`), file storage |
| System design | Full architecture — drawable and explainable end to end |

---

## Current State (Day 2 Complete)

**What exists:**
- `backend/ingestion/models.py` — `DocumentChunk` and `BusinessDocument` Pydantic models with validators
- `backend/config.py` — env vars, chunk size (300), overlap (50), model name
- `backend/` directory structure with stubs for all layers
- `tests/test_models.py` — Day 1 tests passing (run with `python -X utf8 tests/test_models.py`)
- `requirements.txt` — all dependencies listed

**What is next (Day 3–4):**
- `backend/ingestion/loader.py` — `DocumentLoader` class handling CSV, PDF, TXT
- `backend/ingestion/chunker.py` — `SemanticChunker` with word-level chunking and overlap

---

## How to Run Tests

```bash
# From project root
python -X utf8 tests/test_models.py
```

The `-X utf8` flag is required on Windows to handle emoji characters in test output.

---

## Key Design Decisions (Document as you build)

### Chunking
- `chunk_size=300` words, `overlap=50` words (~17%)
- Word-level (not sentence-level) because CSV rows don't have clean sentence boundaries
- Overlap prevents month-boundary records from being split mid-context

### Retrieval
- Hybrid (BM25 + dense vectors) over pure semantic search
- BM25 catches exact product names, dates, numbers that semantic search misses
- RRF fusion combines ranked lists without needing to tune weights

### LLM
- Anthropic Claude API (claude-3-5-haiku for agent loop, claude-3-5-sonnet for quality-critical generation)
- Built retrieval from scratch (no LangChain) — full control, lower latency, easier to explain in interviews

### Evaluation
- RAGAS for automated faithfulness + relevance scoring
- LangSmith for end-to-end tracing
- Golden dataset of 20 QA pairs built from realistic SMB business scenarios

---

## Interview Prep Notes (Add as you build)

For each component you build, be able to answer:
1. What does this do?
2. Why this approach vs alternatives?
3. What are the failure modes?
4. How would you scale this?

---

## Project File Structure

```
SMB_AI_Agent/
├── CLAUDE.md                   ← This file
├── backend/
│   ├── __init__.py
│   ├── main.py                 ← FastAPI app
│   ├── config.py               ← env vars, constants
│   ├── ingestion/
│   │   ├── models.py           ← Pydantic models (DONE)
│   │   ├── loader.py           ← Document loading (next)
│   │   └── chunker.py          ← Chunking logic (next)
│   ├── retrieval/
│   │   ├── vector_store.py     ← ChromaDB + MiniLM
│   │   ├── bm25_retriever.py   ← Sparse retrieval
│   │   └── hybrid_retriever.py ← RRF fusion
│   ├── agents/
│   │   ├── tools.py            ← Tool definitions
│   │   └── business_analyst.py ← ReAct agent loop
│   ├── evaluation/
│   │   └── ragas_eval.py       ← RAGAS pipeline
│   ├── generation/             ← LLM generation layer
│   └── observability/
│       ├── tracer.py           ← LangSmith tracing
│       └── logger.py           ← Structured logging
├── frontend/
│   └── app.py                  ← Gradio UI
├── tests/
│   └── test_models.py          ← Day 1 tests (passing)
├── docs/
│   ├── week1.md                ← Weekly design decisions
│   └── learnings/              ← Daily study notes (Day N format)
├── evaluation/
│   └── golden_dataset.py       ← 20 QA pairs for eval
├── requirements.txt
└── README.md                   ← Public-facing (build in Week 4)
```
