from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
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

chain = prompt | llm


async def run_optimizer_agent(code: str) -> dict:
    response = await chain.ainvoke({"code": code})
    return {
        "agent": "Optimizer",
        "result": response.content
    }