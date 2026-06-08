import httpx
import os
import base64
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

MAX_FILES = 5
MAX_FILE_SIZE = 3000

CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".cpp", ".c", ".rs"}

PRIORITY_PATTERNS = [
    "main", "app", "index", "server", "api", "core",
    "routes", "models", "utils", "helpers", "config"
]

DEPRIORITY_PATTERNS = [
    "test", "spec", "mock", "fixture", "__pycache__",
    "node_modules", "dist", "build", ".min."
]


def parse_repo_url(url: str) -> tuple[str, str]:
    parts = url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo


def priority_score(file_path: str) -> int:
    path_lower = file_path.lower()

    for pattern in DEPRIORITY_PATTERNS:
        if pattern in path_lower:
            return -1

    score = 0
    for pattern in PRIORITY_PATTERNS:
        if pattern in path_lower:
            score += 2

    depth = path_lower.count("/")
    score -= depth

    return score


async def fetch_repo_contents(url: str) -> str:
    owner, repo = parse_repo_url(url)

    async with httpx.AsyncClient() as client:
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        tree_res = await client.get(tree_url, headers=HEADERS)
        tree_res.raise_for_status()
        tree = tree_res.json()

        files = [
            item for item in tree.get("tree", [])
            if item["type"] == "blob"
            and any(item["path"].endswith(ext) for ext in CODE_EXTENSIONS)
            and item.get("size", 0) < MAX_FILE_SIZE
        ]

        files.sort(key=lambda f: priority_score(f["path"]), reverse=True)
        files = [f for f in files if priority_score(f["path"]) >= 0][:MAX_FILES]

        all_content = []
        for file in files:
            file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file['path']}"
            file_res = await client.get(file_url, headers=HEADERS)
            if file_res.status_code == 200:
                content = file_res.json().get("content", "")
                decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
                all_content.append(f"### FILE: {file['path']}\n{decoded}")

        return "\n\n".join(all_content)