# citral-pipeline — CLAUDE.md

> **Project docs:** See [citral-ai/docs](https://github.com/citral-ai/docs) for full product architecture, tech stack, and decisions.

## What This Is

The AI pipeline service for Citral — a **Python gRPC service** that runs the BMR auditing pipeline. It receives jobs from the Go job-manager via gRPC, runs the AI pipeline, and streams results back.

**This service only does AI work.** It does NOT handle HTTP, auth, file storage, users, or SOPs. Those are Go services.

## Pipeline Flow

```
Receives gRPC AuditRequest (audit_id, document_url, sop_content)
  → Download PDF from URL
  → PageIndex builds document tree
  → Docling/PyMuPDF extracts text per tree node
  → Build shared context from tree
  → N parallel auditor agents (asyncio.TaskGroup + Claude SDK)
  → Conclusion agent synthesizes findings
  → Stream results back via gRPC AuditEvent stream
```

## Tech Stack

- **Language:** Python 3.12
- **Communication:** gRPC (receives jobs from Go job-manager)
- **LLM:** Anthropic Claude (async SDK) — Sonnet for auditors, configurable
- **Document Intelligence:** PageIndex (tree indexing) + Docling (text extraction)
- **Concurrency:** asyncio.TaskGroup with Semaphore for rate limiting

## Project Structure

```
proto/
└── pipeline.proto          # gRPC service definition (shared with Go services)
app/
├── main.py                 # gRPC server entrypoint
├── config.py               # Settings (model, concurrency, etc.)
└── pipeline/
    ├── orchestrator.py     # Full pipeline coordination
    ├── indexer.py          # PageIndex integration
    ├── extractor.py        # Docling/PyMuPDF text extraction
    ├── auditor.py          # Parallel Claude auditor agents
    ├── conclusion.py       # Conclusion agent
    └── reporter.py         # Report data formatting
```

## Commands

```bash
pip install -e ".[dev]"                    # Install deps
python -m app.main                          # Run gRPC server
python -m grpc_tools.protoc -I proto \      # Generate proto stubs
  --python_out=. --grpc_python_out=. proto/pipeline.proto
pytest                                      # Tests
ruff check . && ruff format .               # Lint + format
```

## gRPC Interface

- **Input:** `AuditRequest` — audit_id, document_url (R2), sop_content, config
- **Output:** Stream of `AuditEvent` — status updates, tree, section results, conclusion
- **Proto:** `proto/pipeline.proto`

## Key Design Rules

- Every auditor finding MUST cite source text verbatim
- Temperature 0 on all LLM calls for reproducibility
- Semaphore limits concurrent Claude API calls
- All LLM I/O logged: model_id, tokens_used, prompt_hash
