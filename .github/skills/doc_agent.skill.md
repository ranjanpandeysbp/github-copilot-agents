---
name: doc_agent
description: Interactive skill to collect repository URLs and PAT token, then invoke the download tool.
entrypoint: doc_agent:run
---

This skill greets the user and guides them through repository download configuration.

Flow:
- Greet the user.
- Ask the user to provide or confirm:
  - `REPOS`: Comma-separated array of GitHub repository URLs (e.g., https://github.com/owner/repo1, https://github.com/owner/repo2)
  - `REPO_TOKEN`: GitHub personal access token for authentication
- Confirm the values before proceeding.
- After confirmation, call the `download_repos_tool` with `env` pointing to the workspace `.env` and `dest` set to `temp`.

Notes for implementers:
- This skill is a conversational wrapper; the actual cloning/download is performed by [sample/.github/tools/download_repos.py](sample/.github/tools/download_repos.py).
- It should read or create the `.env` file in the workspace root when the user provides values, then invoke the tool.
- Validate that at least one repository URL is provided before invoking the download tool.
