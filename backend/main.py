from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.github_fetcher import fetch_repo_contents
from services.orchestrator import run_all_agents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    repo_url: str


@app.get("/")
async def root():
    return {"status": "Code Review Agent API is running"}


@app.post("/review")
async def review_repo(request: ReviewRequest):
    try:
        code = await fetch_repo_contents(request.repo_url)

        if not code:
            raise HTTPException(status_code=400, detail="No code files found in this repository")

        results = await run_all_agents(code)
        return {
            "repo_url": request.repo_url,
            "agents": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))