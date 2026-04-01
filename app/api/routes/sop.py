from fastapi import APIRouter

router = APIRouter(tags=["sop"])


@router.get("/sops")
async def list_sops():
    """List all SOPs for the current tenant."""
    # TODO: fetch from database
    return {"sops": []}


@router.post("/sops")
async def create_sop():
    """Create or update an SOP."""
    # TODO: implement
    return {"message": "not implemented"}
