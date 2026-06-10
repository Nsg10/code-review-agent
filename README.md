# CodeLens — Multi-Agent AI Code Review System

> Paste any public GitHub repository URL and get an instant multi-perspective AI code review from 4 specialized agents running in parallel.

**[Live Demo](https://code-review-agent-2wnwxm6gw-niharika-s-projects4.vercel.app)** · **[Backend API](https://code-review-agent-api-ovr9.onrender.com)**

---

## What It Does

CodeLens analyzes any public GitHub repository through 4 parallel AI agents:

| Agent | What It Reviews |
|---|---|
| ⚙️ Code Quality | Style, maintainability, best practices — scored 1–10 |
| 🐛 Bug Detector | Potential bugs with file/line references and fixes |
| ⚡ Optimizer | Performance bottlenecks and refactoring opportunities |
| 🏗️ System Design | Architecture, coupling, scalability recommendations |

All 4 agents run simultaneously via `asyncio.gather()` — total review time ~5 seconds.

---

## Architecture

1. User pastes GitHub URL → React Frontend (Vercel)
2. Frontend sends POST /review → FastAPI Backend (Render)
3. Backend fetches top 5 files via GitHub API (smart prioritization)
4. LangChain Orchestrator runs 4 agents in parallel via asyncio.gather()
   ├── Agent 1: Code Quality  (Groq LLaMA 3.1)
   ├── Agent 2: Bug Detector  (Groq LLaMA 3.1)
   ├── Agent 3: Optimizer     (Groq LLaMA 3.1)
   └── Agent 4: System Design (Groq LLaMA 3.1)
5. Merged JSON response → React Dashboard
6. Ratings + review counter saved to Supabase

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI + Python |
| AI Orchestration | LangChain |
| LLM | Groq free tier (llama-3.1-8b-instant) |
| Memory | Supabase (ratings + persistent counter) |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |

**Total infrastructure cost: $0**

---

## Key Technical Decisions

**Parallel execution** — `asyncio.gather()` runs all 4 Groq API calls simultaneously. Total latency = slowest single agent (~3–5s) instead of 4× sequential (~20s).

**Smart file prioritization** — Files scored by entry-point patterns (`main`, `app`, `index`, `server`, `api`) and penalized by directory depth and test/build patterns. Top 5 files selected for review.

**Token budgeting** — 5 file cap + 3KB per file keeps requests within Groq's free tier TPM limits while giving agents enough context for meaningful reviews.

**Structured prompt format** — Each agent returns output in a strict labeled format (SCORE, SUMMARY, ISSUES, RECOMMENDATIONS) enabling consistent frontend parsing and rendering.

**Graceful degradation** — Each agent has independent error handling. If one agent hits a rate limit, the other 3 still return results. The failed agent returns a clean error message instead of crashing the pipeline.

---

## Running Locally

**Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add GROQ_API_KEY, GITHUB_TOKEN, SUPABASE_URL, SUPABASE_KEY
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
cp .env.example .env  # add VITE_API_URL=http://127.0.0.1:8000
npm run dev
```

**Tests**
```bash
cd backend
pytest -v
```

---

## Project Structure

```
code-review-agent/
├── frontend/                    # React + Vite → Vercel
│   └── src/
│       ├── components/          # AgentCard, Dashboard, UrlInput, LoadingState
│       ├── hooks/               # useReview (API state management)
│       └── utils/               # parseResult (structured output parser)
│
└── backend/                     # FastAPI → Render
    ├── agents/                  # 4 LangChain + Groq agents
    ├── services/
    │   ├── github_fetcher.py    # Smart file prioritization
    │   ├── orchestrator.py      # asyncio.gather() parallel execution
    │   └── supabase_client.py   # Persistent counter + ratings
    ├── tests/                   # 10 pytest tests
    └── main.py                  # FastAPI routes + rate limiting
```

---

## Features

- 4 parallel AI agents with independent error handling
- Smart file prioritization — entry points first, tests/dist skipped
- Rate limiting — 5 requests/hour per IP via `slowapi`
- Persistent review counter via Supabase
- Thumbs up/down agent ratings saved to Supabase
- Score rings with color coding (green ≥8, amber ≥6, red <6)
- Expandable structured review cards
- Copy button per agent card

---

Built by [Niharika](https://github.com/Nsg10) · AI Intern at F-Secure · B.E. AIML @ CMRIT Bengaluru
