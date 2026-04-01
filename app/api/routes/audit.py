from fastapi import APIRouter, UploadFile

router = APIRouter(tags=["audit"])


@router.post("/audit")
async def create_audit(file: UploadFile):
    """Upload a BMR PDF and start an audit job."""
    # TODO: validate file, store in R2, create job, start pipeline
    return {
        "job_id": "placeholder",
        "status": "pending",
        "filename": file.filename,
    }


@router.get("/audit/{audit_id}")
async def get_audit(audit_id: str):
    """Get audit status and results."""
    # TODO: fetch from database
    return {"audit_id": audit_id, "status": "pending"}


@router.get("/audit/{audit_id}/report")
async def get_report(audit_id: str):
    """Download the audit report (PDF/JSON)."""
    # TODO: fetch report from storage
    return {"audit_id": audit_id, "message": "not implemented"}


@router.get("/audit/{audit_id}/tree")
async def get_tree(audit_id: str):
    """Get the PageIndex document tree."""
    # TODO: fetch tree from database
    return {"audit_id": audit_id, "tree": None}


@router.get("/audits")
async def list_audits():
    """List all audits for the current tenant."""
    # TODO: fetch from database with tenant filter
    return {"audits": []}
