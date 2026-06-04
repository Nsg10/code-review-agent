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
    ("system", """You are a senior software engineer specializing in finding bugs.
Analyze the provided code and return your review in this exact format:

SEVERITY: (High / Medium / Low)
SUMMARY: (2-3 sentences overview)
BUGS FOUND:
- (bug 1 — file and line if possible)
- (bug 2 — file and line if possible)
- (bug 3 — file and line if possible)
FIXES:
- (fix 1)
- (fix 2)
- (fix 3)

Be specific. Reference actual code."""),
    ("human", "Find bugs in this code:\n\n{code}")
])

chain = prompt | llm


async def run_bug_detector_agent(code: str) -> dict:
    response = await chain.ainvoke({"code": code})
    return {
        "agent": "Bug Detector",
        "result": response.content
    }