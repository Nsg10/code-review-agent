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
    ("system", """You are a senior software engineer reviewing code quality.
Analyze the provided code and return your review in this exact format:

SCORE: (a number from 1-10)
SUMMARY: (2-3 sentences overview)
ISSUES:
- (issue 1)
- (issue 2)
- (issue 3)
RECOMMENDATIONS:
- (recommendation 1)
- (recommendation 2)
- (recommendation 3)

Be specific and actionable. Reference actual code from the files."""),
    ("human", "Review this code:\n\n{code}")
])


async def run_code_quality_agent(code: str) -> dict:
    try:
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({"code": code})
        return {
            "agent": "Code Quality",
            "result": response.content
        }
    except Exception as e:
        error_str = str(e)
        if "rate_limit" in error_str.lower() or "429" in error_str:
            return {
                "agent": "Code Quality",
                "result": "SCORE: N/A\nSUMMARY: Rate limit reached on Groq free tier. Please wait a moment and try again.\nISSUES:\n- Rate limit exceeded\nRECOMMENDATIONS:\n- Try again in 60 seconds"
            }
        return {
            "agent": "Code Quality",
            "result": f"SCORE: N/A\nSUMMARY: Agent encountered an error: {error_str}\nISSUES:\n- Agent failed\nRECOMMENDATIONS:\n- Try again"
        }