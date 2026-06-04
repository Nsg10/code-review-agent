import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

MAX_FILES = 10
MAX_FILE_SIZE = 50000  # 50KB per file


def parse_repo_url(url: str) -> tuple[str, str]:
    parts = url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo


async def fetch_repo_contents(url: str) -> str:
    owner, repo = parse_repo_url(url)

    async with httpx.AsyncClient() as client:
        # Get file tree
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        tree_res = await client.get(tree_url, headers=HEADERS)
        tree_res.raise_for_status()
        tree = tree_res.json()

        # Filter to code files only
        code_extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".cpp", ".c", ".rs"}
        files = [
            item for item in tree.get("tree", [])
            if item["type"] == "blob"
            and any(item["path"].endswith(ext) for ext in code_extensions)
            and item.get("size", 0) < MAX_FILE_SIZE
        ][:MAX_FILES]

        # Fetch file contents
        all_content = []
        for file in files:
            file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file['path']}"
            file_res = await client.get(file_url, headers=HEADERS)
            if file_res.status_code == 200:
                import base64
                content = file_res.json().get("content", "")
                decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
                all_content.append(f"### FILE: {file['path']}\n{decoded}")

        return "\n\n".join(all_content)