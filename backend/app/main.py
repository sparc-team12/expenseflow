from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.domain.claim_rules import validate_claim, next_status

app = FastAPI(title="ExpenseFlow")

# In-memory storage. We swap this for DynamoDB on Day 2.
CLAIMS: dict[str, dict] = {}


class ClaimIn(BaseModel):
    employee: str
    amount: float
    category: str
    description: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/claims")
def create_claim(payload: ClaimIn):
    errors = validate_claim(payload.amount, payload.category, payload.description)
    if errors:
        raise HTTPException(status_code=400, detail=errors)

    claim = {"id": uuid4().hex[:8], "status": "submitted", **payload.model_dump()}
    CLAIMS[claim["id"]] = claim
    return claim


@app.get("/api/claims")
def list_claims():
    return list(CLAIMS.values())


@app.post("/api/claims/{claim_id}/{action}")
def act_on_claim(claim_id: str, action: str):
    if action not in ("approve", "reject"):
        raise HTTPException(status_code=404, detail="Unknown action")

    claim = CLAIMS.get(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    try:
        claim["status"] = next_status(claim["status"], action)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return claim


# Serve the UI. This mount MUST stay last, or it swallows the /api routes.
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="ui")