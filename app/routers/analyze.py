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

@router.get("/api/test-openai")
async def test_openai():
    import openai
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        return {"error": "No API key found in environment"}
    try:
        client = openai.AsyncOpenAI(api_key=key)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=5
        )
        return {"success": True, "response": response.choices[0].message.content}
    except Exception as e:
        return {"error": type(e).__name__, "detail": str(e)}

@router.post("/api/analyze")
async def analyze(req: PostingRequest):
    if not req.text or len(req.text.strip()) < 30:
        return {"error": "Please paste a full job posting (at least 30 characters)."}
    result = await analyze_posting(req.text.strip())
    return result
