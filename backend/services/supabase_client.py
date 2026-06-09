import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def get_total_reviews() -> int:
    try:
        response = supabase.table("review_stats").select("total_reviews").eq("id", 1).execute()
        return response.data[0]["total_reviews"]
    except Exception:
        return 0


async def increment_review_count() -> int:
    try:
        current = await get_total_reviews()
        new_count = current + 1
        supabase.table("review_stats").update({"total_reviews": new_count}).eq("id", 1).execute()
        return new_count
    except Exception:
        return 0


async def save_rating(repo_url: str, agent_name: str, rating: int) -> bool:
    try:
        supabase.table("agent_ratings").insert({
            "repo_url": repo_url,
            "agent_name": agent_name,
            "rating": rating
        }).execute()
        return True
    except Exception:
        return False