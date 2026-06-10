import pytest
from unittest.mock import AsyncMock, patch
from services.orchestrator import run_all_agents


@pytest.mark.asyncio
async def test_run_all_agents_returns_four_results():
    mock_result = {"agent": "Test", "result": "Test result"}

    with patch("services.orchestrator.run_code_quality_agent", new=AsyncMock(return_value={"agent": "Code Quality", "result": "SCORE: 8\nSUMMARY: Good code."})), \
         patch("services.orchestrator.run_bug_detector_agent", new=AsyncMock(return_value={"agent": "Bug Detector", "result": "SEVERITY: Low\nSUMMARY: No bugs."})), \
         patch("services.orchestrator.run_optimizer_agent", new=AsyncMock(return_value={"agent": "Optimizer", "result": "PERFORMANCE_SCORE: 7\nSUMMARY: Good performance."})), \
         patch("services.orchestrator.run_system_design_agent", new=AsyncMock(return_value={"agent": "System Design", "result": "ARCHITECTURE_SCORE: 8\nSUMMARY: Good architecture."})):

        results = await run_all_agents("sample code")

    assert len(results) == 4
    agent_names = [r["agent"] for r in results]
    assert "Code Quality" in agent_names
    assert "Bug Detector" in agent_names
    assert "Optimizer" in agent_names
    assert "System Design" in agent_names


@pytest.mark.asyncio
async def test_run_all_agents_handles_failure():
    with patch("services.orchestrator.run_code_quality_agent", new=AsyncMock(side_effect=Exception("Groq error"))), \
         patch("services.orchestrator.run_bug_detector_agent", new=AsyncMock(return_value={"agent": "Bug Detector", "result": "SEVERITY: Low\nSUMMARY: No bugs."})), \
         patch("services.orchestrator.run_optimizer_agent", new=AsyncMock(return_value={"agent": "Optimizer", "result": "PERFORMANCE_SCORE: 7\nSUMMARY: Good."})), \
         patch("services.orchestrator.run_system_design_agent", new=AsyncMock(return_value={"agent": "System Design", "result": "ARCHITECTURE_SCORE: 8\nSUMMARY: Good."})):

        results = await run_all_agents("sample code")

    assert len(results) == 4
    failed = next(r for r in results if r["agent"] == "Code Quality")
    assert "failed" in failed["result"].lower() or "Agent failed" in failed["result"]


@pytest.mark.asyncio
async def test_run_all_agents_empty_code():
    with patch("services.orchestrator.run_code_quality_agent", new=AsyncMock(return_value={"agent": "Code Quality", "result": "SCORE: 1\nSUMMARY: Empty code."})), \
         patch("services.orchestrator.run_bug_detector_agent", new=AsyncMock(return_value={"agent": "Bug Detector", "result": "SEVERITY: Low\nSUMMARY: Empty."})), \
         patch("services.orchestrator.run_optimizer_agent", new=AsyncMock(return_value={"agent": "Optimizer", "result": "PERFORMANCE_SCORE: 1\nSUMMARY: Empty."})), \
         patch("services.orchestrator.run_system_design_agent", new=AsyncMock(return_value={"agent": "System Design", "result": "ARCHITECTURE_SCORE: 1\nSUMMARY: Empty."})):

        results = await run_all_agents("")

    assert len(results) == 4