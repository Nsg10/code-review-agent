from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from services.github_fetcher import fetch_repo_contents
from services.orchestrator import run_all_agents
from services.supabase_client import get_total_reviews, increment_review_count, save_rating

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    repo_url: str


class RatingRequest(BaseModel):
    repo_url: str
    agent_name: str
    rating: int


@app.get("/")
async def root():
    return {"status": "Code Review Agent API is running"}


@app.get("/stats")
async def get_stats():
    total = await get_total_reviews()
    return {"total_reviews": total}


@app.post("/rate")
async def rate_agent(body: RatingRequest):
    if body.rating not in [1, -1]:
        raise HTTPException(status_code=400, detail="Rating must be 1 or -1")
    success = await save_rating(body.repo_url, body.agent_name, body.rating)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save rating")
    return {"status": "ok"}


@app.post("/review")
@limiter.limit("5/hour")
async def review_repo(request: Request, body: ReviewRequest):
    try:
        code = await fetch_repo_contents(body.repo_url)

        if not code:
            raise HTTPException(
                status_code=400,
                detail="No code files found in this repository"
            )

        results = await run_all_agents(code)
        total_reviews = await increment_review_count()

        return {
            "repo_url": body.repo_url,
            "agents": results,
            "total_reviews": total_reviews
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))