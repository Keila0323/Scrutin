import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.scanner import analyze_posting

router = APIRouter()

class PostingRequest(BaseModel):
    text: str

@router.get("/api/health")
async def health():
    key = os.getenv("OPENAI_API_KEY", "")
    return {
        "status": "ok",
        "openai_key_set": bool(key),
        "key_preview": key[:8] + "..." if key else "NOT SET"
    }

@router.post("/api/analyze")
async def analyze(req: PostingRequest):
    if not req.text or len(req.text.strip()) < 30:
        return {"error": "Please paste a full job posting (at least 30 characters)."}
    result = await analyze_posting(req.text.strip())
    return result
