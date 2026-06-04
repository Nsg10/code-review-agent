import asyncio
from agents.code_quality import run_code_quality_agent
from agents.bug_detector import run_bug_detector_agent
from agents.optimizer import run_optimizer_agent
from agents.system_design import run_system_design_agent


async def run_all_agents(code: str) -> list:
    results = await asyncio.gather(
        run_code_quality_agent(code),
        run_bug_detector_agent(code),
        run_optimizer_agent(code),
        run_system_design_agent(code),
        return_exceptions=True
    )

    # Handle any agent that failed
    agents = ["Code Quality", "Bug Detector", "Optimizer", "System Design"]
    cleaned = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            cleaned.append({
                "agent": agents[i],
                "result": f"Agent failed: {str(result)}"
            })
        else:
            cleaned.append(result)

    return cleaned