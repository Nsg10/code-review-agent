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
    ("system", """You are a senior software architect specializing in system design.
Analyze the provided code and return your review in this exact format:

ARCHITECTURE_SCORE: (a number from 1-10)
SUMMARY: (2-3 sentences overview)
DESIGN_ISSUES:
- (issue 1)
- (issue 2)
- (issue 3)
SCALABILITY_RECOMMENDATIONS:
- (recommendation 1)
- (recommendation 2)
- (recommendation 3)

Be specific. Reference actual code and architecture patterns."""),
    ("human", "Review the system design of this code:\n\n{code}")
])


async def run_system_design_agent(code: str) -> dict:
    try:
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({"code": code})
        return {
            "agent": "System Design",
            "result": response.content
        }
    except Exception as e:
        error_str = str(e)
        if "rate_limit" in error_str.lower() or "429" in error_str:
            return {
                "agent": "System Design",
                "result": "ARCHITECTURE_SCORE: N/A\nSUMMARY: Rate limit reached on Groq free tier. Please wait a moment and try again.\nDESIGN_ISSUES:\n- Rate limit exceeded\nSCALABILITY_RECOMMENDATIONS:\n- Try again in 60 seconds"
            }
        return {
            "agent": "System Design",
            "result": f"ARCHITECTURE_SCORE: N/A\nSUMMARY: Agent encountered an error: {error_str}\nDESIGN_ISSUES:\n- Agent failed\nSCALABILITY_RECOMMENDATIONS:\n- Try again"
        }