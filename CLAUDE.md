# citral-pipeline — CLAUDE.md

> **Project docs:** See [citral-ai/docs](https://github.com/citral-ai/docs) for full product architecture, tech stack, and decisions.

## What This Is

The core Citral service — a Python FastAPI application that audits pharmaceutical BMR documents using AI.

**Pipeline:** Upload PDF → PageIndex builds document tree → Docling extracts text → N parallel Claude auditor agents → Conclusion agent → PDF/JSON report

## Tech Stack

- **Framework:** Python FastAPI
- **LLM:** Anthropic Claude (Sonnet 4 for auditors, Haiku 3.5 for sub-tasks)
- **Document Intelligence:** PageIndex (tree indexing) + Docling (text/table extraction)
- **Database:** PostgreSQL via Neon (serverless)
- **Auth:** Clerk
- **File Storage:** Cloudflare R2 (S3-compatible)
- **Concurrency:** asyncio.TaskGroup + Anthropic async SDK

## Project Structure

```
app/
├── main.py              # FastAPI app entrypoint
├── config.py            # Environment-based settings
├── api/
│   └── routes/          # API route handlers
│       ├── audit.py     # /api/v1/audit endpoints
│       ├── sop.py       # /api/v1/sops endpoints
│       └── health.py    # /healthz, /readyz
├── pipeline/            # Core audit pipeline
│   ├── orchestrator.py  # Job orchestration + state machine
│   ├── indexer.py       # PageIndex integration
│   ├── extractor.py     # Docling/PyMuPDF text extraction
│   ├── auditor.py       # Parallel auditor agents (Claude)
│   ├── conclusion.py    # Conclusion agent
│   └── reporter.py      # Report generation (JSON → HTML → PDF)
├── models/              # SQLAlchemy/Pydantic models
│   ├── audit.py
│   ├── section.py
│   ├── sop.py
│   └── user.py
├── db/                  # Database
│   ├── session.py       # DB connection
│   └── migrations/      # Alembic migrations
└── services/            # External service integrations
    ├── storage.py       # R2/S3 file storage
    └── llm.py           # Claude API wrapper
```

## Commands

```bash
# Install dependencies
pip install -e ".[dev]"

# Run locally
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Database migrations
alembic upgrade head

# Lint
ruff check .

# Format
ruff format .
```

## Environment Variables

```
DATABASE_URL=postgresql://...          # Neon connection string
ANTHROPIC_API_KEY=sk-ant-...           # Claude API key
R2_ENDPOINT=https://...r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=citral-documents
CLERK_SECRET_KEY=sk_...                # Clerk auth
```
