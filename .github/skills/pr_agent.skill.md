---
name: pr_agent
description: Interactive skill to choose between full repo download or PR-only download, then invoke the download tool.
entrypoint: pr_agent:run
---

This skill greets the user and asks whether they'd like to run a full-repo download or a PR-only download.

Flow:
- Greet the user.
- Ask: "Do you want full repo download or PR review only?" (choices: Full, PR)
- If PR: ask user to provide or confirm `PR_URL` and `REPO_TOKEN` if needed. Confirm before proceeding.
- If Full: ask user to provide `REPOS` array (comma-separated) and optional `REPO_TOKEN`. Confirm before proceeding.
- After confirmation, call the `download_repos_tool` with `env` pointing to the workspace `.env` (or use provided values) and `dest` set to `temp`.

Notes for implementers:
- This skill is a conversational wrapper; the actual cloning/download is performed by [sample/.github/tools/download_repos.py](sample/.github/tools/download_repos.py).
- It should update or create a temporary `.env` in the workspace root when the user provides values, then invoke the tool.
