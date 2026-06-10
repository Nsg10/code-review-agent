import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.github_fetcher import parse_repo_url, priority_score, fetch_repo_contents


def test_parse_repo_url_standard():
    owner, repo = parse_repo_url("https://github.com/facebook/react")
    assert owner == "facebook"
    assert repo == "react"


def test_parse_repo_url_trailing_slash():
    owner, repo = parse_repo_url("https://github.com/vercel/next.js/")
    assert owner == "vercel"
    assert repo == "next.js"


def test_priority_score_high_priority():
    score = priority_score("src/main.py")
    assert score > 0


def test_priority_score_deprioritized():
    score = priority_score("tests/test_main.py")
    assert score < 0


def test_priority_score_node_modules():
    score = priority_score("node_modules/react/index.js")
    assert score < 0


def test_priority_score_deep_file():
    shallow = priority_score("app.py")
    deep = priority_score("a/b/c/d/app.py")
    assert shallow > deep


@pytest.mark.asyncio
async def test_fetch_repo_contents_returns_string():
    mock_tree = {
        "tree": [
            {"type": "blob", "path": "main.py", "size": 500},
        ]
    }
    mock_file = {
        "content": "cHJpbnQoJ2hlbGxvJyk="
    }

    mock_response_tree = MagicMock()
    mock_response_tree.json.return_value = mock_tree
    mock_response_tree.raise_for_status = MagicMock()

    mock_response_file = MagicMock()
    mock_response_file.json.return_value = mock_file
    mock_response_file.status_code = 200

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[mock_response_tree, mock_response_file])

    with patch("services.github_fetcher.httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value = mock_client
        mock_async_client.return_value.__aexit__.return_value = AsyncMock()
        result = await fetch_repo_contents("https://github.com/test/repo")

    assert isinstance(result, str)
    assert "main.py" in result