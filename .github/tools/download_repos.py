#!/usr/bin/env python3
"""Download multiple git repos listed in a .env file into the workspace root `temp/` folder.

Behavior:
- Reads `.env` from the workspace root (parent of the `tools` folder) or environment variables.
- Expects `REPOS` to be a comma-separated list of HTTPS repo URLs.
- If a clone fails and `REPO_TOKEN` is available, the script will retry using the token inserted into the URL for GitHub private repos.

Usage:
    python tools/download_repos.py
    python tools/download_repos.py --env .env --dest temp

"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import json
import urllib.request
import urllib.error


def load_env(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('\"').strip("\'")
        env[key] = val
    return env


def parse_repos(raw: str) -> List[str]:
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    parts = [p.strip().strip('\"').strip("\'") for p in raw.split(",")]
    return [p for p in parts if p]


def run(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    print("$", " ".join(shlex.quote(p) for p in cmd))
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def owner_and_repo_from_url(url: str) -> Optional[tuple[str, str, str]]:
    # Expect URL like: https://github.com/owner/repo(.git)
    try:
        # strip protocol
        if url.startswith("https://"):
            tail = url[len("https://"):]
        elif url.startswith("http://"):
            tail = url[len("http://"):]
        else:
            tail = url
        # remove possible credentials
        if "@" in tail:
            tail = tail.split("@", 1)[1]
        parts = tail.split("/")
        host = parts[0]
        if len(parts) >= 3:
            owner = parts[1]
            repo = parts[2]
            return owner, repo, host
    except Exception:
        return None
    return None


def build_auth_url(orig_url: str, token: str) -> Optional[str]:
    parsed = owner_and_repo_from_url(orig_url)
    if not parsed:
        return None
    owner, repo, host = parsed
    path = orig_url.split(host, 1)[1]
    # include token as username:token@host
    return f"https://{owner}:{token}@{host}{path}"


def clone_or_pull(repo_url: str, dest_parent: Path, token: Optional[str]) -> None:
    parsed = owner_and_repo_from_url(repo_url)
    if not parsed:
        print(f"Skipping invalid URL: {repo_url}")
        return
    _, repo_with_git, _ = parsed
    repo_name = repo_with_git[:-4] if repo_with_git.endswith('.git') else repo_with_git
    dest = dest_parent / repo_name

    if dest.exists():
        print(f"Updating existing repo {repo_name} in {dest}")
        res = run(["git", "-C", str(dest), "pull"])
        if res.returncode == 0:
            print(res.stdout)
            return
        print("Pull failed:", res.stderr)
        # fall through to try cloning into a temp location

    print(f"Cloning {repo_url} into {dest}")
    # first try cloning directly
    res = run(["git", "clone", repo_url, str(dest_parent / repo_name)])
    if res.returncode == 0:
        print(res.stdout)
        return

    print(f"Initial clone failed for {repo_name}:", res.stderr)
    # if token is provided and host is github.com, retry with token
    if token:
        auth = build_auth_url(repo_url, token)
        if auth:
            print("Retrying with auth token for private repo...")
            res2 = run(["git", "clone", auth, str(dest_parent / repo_name)])
            if res2.returncode == 0:
                print(res2.stdout)
                return
            print(f"Clone with token also failed: {res2.stderr}")

    print(f"Failed to download {repo_url}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clone multiple repos listed in a .env REPOS variable into temp/")
    parser.add_argument("--env", default=None, help="Path to .env file (defaults to workspace root .env)")
    parser.add_argument("--dest", default="temp", help="Destination folder name under workspace root")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    # workspace root should be the directory that contains the `.github` folder
    # (one level up from the `.github` directory), so go up an extra level.
    workspace_root = script_dir.parent.parent

    env_path = Path(args.env) if args.env else workspace_root / ".env"
    env = load_env(env_path)

    # Allow environment variables to override .env
    REPOS_raw = env.get("REPOS") or os.environ.get("REPOS") or ""
    REPO_TOKEN = env.get("REPO_TOKEN") or os.environ.get("REPO_TOKEN")
    MODE = env.get("MODE") or os.environ.get("MODE")
    PR_URL = env.get("PR_URL") or os.environ.get("PR_URL")

    # If MODE=PR, ignore REPOS and download only files modified in the PR
    dest_root = workspace_root / args.dest
    dest_root.mkdir(parents=True, exist_ok=True)

    if MODE and MODE.upper() == "PR":
        if not PR_URL:
            print("MODE=PR set but PR_URL not found in .env or environment variables.")
            return
        download_pr_modified_files(PR_URL, dest_root, REPO_TOKEN)
        return

    repos = parse_repos(REPOS_raw)
    if not repos:
        print("No repos found. Please set REPOS in .env or environment variables.")
        return

    for r in repos:
        clone_or_pull(r, dest_root, REPO_TOKEN)


def parse_pr_url(pr_url: str) -> Optional[tuple[str, str, str, int]]:
    # Expect URL like: https://github.com/owner/repo/pull/2
    parsed = owner_and_repo_from_url(pr_url)
    if not parsed:
        return None
    owner, repo, host = parsed
    # extract pull number
    try:
        if "/pull/" in pr_url:
            pull_part = pr_url.split("/pull/", 1)[1]
            pull_num_str = pull_part.split("/", 1)[0]
            pr_number = int(pull_num_str)
            return owner, repo, host, pr_number
    except Exception:
        return None
    return None


def github_api_get(url: str, token: Optional[str]) -> tuple[int, dict, dict]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            encoding = resp.headers.get_content_charset() or "utf-8"
            text = data.decode(encoding, errors="replace")
            return resp.getcode(), json.loads(text), dict(resp.getheaders())
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
            return e.code, json.loads(body) if body else {}, dict(e.headers)
        except Exception:
            return e.code, {}, dict(e.headers)
    except Exception:
        return 0, {}, {}


def fetch_pr_files(owner: str, repo: str, pr_number: int, host: str, token: Optional[str]) -> List[dict]:
    # Use GitHub API to list PR files. Handle pagination.
    api_base = f"https://api.{host}" if not host.endswith("github.com") else "https://api.github.com"
    files: List[dict] = []
    per_page = 100
    page = 1
    while True:
        url = f"{api_base}/repos/{owner}/{repo}/pulls/{pr_number}/files?per_page={per_page}&page={page}"
        code, payload, headers = github_api_get(url, token)
        if code != 200:
            print(f"Failed to fetch PR files: HTTP {code}")
            break
        if not isinstance(payload, list):
            break
        files.extend(payload)
        if len(payload) < per_page:
            break
        page += 1
    return files


def count_patch_changes(patch: Optional[str]) -> tuple[int, int]:
    added = 0
    removed = 0
    if not patch:
        return 0, 0
    for line in patch.splitlines():
        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            continue
        if line.startswith('+'):
            added += 1
        elif line.startswith('-'):
            removed += 1
    return added, removed


def download_pr_modified_files(pr_url: str, dest_parent: Path, token: Optional[str]) -> None:
    parsed = parse_pr_url(pr_url)
    if not parsed:
        print(f"Invalid PR URL: {pr_url}")
        return
    owner, repo, host, pr_number = parsed
    print(f"Fetching PR #{pr_number} files for {owner}/{repo} from {host}")
    files = fetch_pr_files(owner, repo, pr_number, host, token)
    if not files:
        print("No modified files found or failed to fetch PR files.")
        return

    repo_name = repo[:-4] if repo.endswith('.git') else repo
    dest_repo = dest_parent / repo_name
    for f in files:
        filename = f.get('filename')
        patch = f.get('patch')
        raw_url = f.get('raw_url') or f.get('contents_url')
        added, removed = count_patch_changes(patch)
        print(f"File: {filename} (+{added}/-{removed})")
        # create local path and fetch raw content
        local_path = dest_repo / filename
        local_path.parent.mkdir(parents=True, exist_ok=True)
        if raw_url:
            # raw_url for PR file points to the content in the PR head; fetch with token if needed
            try:
                headers = {}
                if token:
                    headers['Authorization'] = f"token {token}"
                req = urllib.request.Request(raw_url, headers=headers)
                with urllib.request.urlopen(req) as resp:
                    data = resp.read()
                    # write bytes
                    with open(local_path, 'wb') as out_f:
                        out_f.write(data)
                print(f"Wrote {local_path}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
        else:
            print(f"No raw URL for {filename}; skipping download.")



if __name__ == "__main__":
    main()
