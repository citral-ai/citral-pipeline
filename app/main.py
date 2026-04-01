from fastapi import FastAPI

from app.api.routes import audit, health, sop

app = FastAPI(
    title="Citral Pipeline",
    description="AI-powered BMR auditing pipeline",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(audit.router, prefix="/api/v1")
app.include_router(sop.router, prefix="/api/v1")
