from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.3
    )

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior software engineer specializing in code optimization.
Analyze the provided code and return your review in this exact format:

PERFORMANCE_SCORE: (a number from 1-10)
SUMMARY: (2-3 sentences overview)
OPTIMIZATIONS:
- (optimization 1 — include time/space complexity improvement if applicable)
- (optimization 2)
- (optimization 3)
REFACTORING_SUGGESTIONS:
- (suggestion 1)
- (suggestion 2)
- (suggestion 3)

Be specific. Reference actual code."""),
    ("human", "Suggest optimizations for this code:\n\n{code}")
])


async def run_optimizer_agent(code: str) -> dict:
    try:
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({"code": code})
        return {
            "agent": "Optimizer",
            "result": response.content
        }
    except Exception as e:
        error_str = str(e)
        if "rate_limit" in error_str.lower() or "429" in error_str:
            return {
                "agent": "Optimizer",
                "result": "PERFORMANCE_SCORE: N/A\nSUMMARY: Rate limit reached on Groq free tier. Please wait a moment and try again.\nOPTIMIZATIONS:\n- Rate limit exceeded\nREFACTORING_SUGGESTIONS:\n- Try again in 60 seconds"
            }
        return {
            "agent": "Optimizer",
            "result": f"PERFORMANCE_SCORE: N/A\nSUMMARY: Agent encountered an error: {error_str}\nOPTIMIZATIONS:\n- Agent failed\nREFACTORING_SUGGESTIONS:\n- Try again"
        }