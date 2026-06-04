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

chain = prompt | llm


async def run_code_quality_agent(code: str) -> dict:
    response = await chain.ainvoke({"code": code})
    return {
        "agent": "Code Quality",
        "result": response.content
    }