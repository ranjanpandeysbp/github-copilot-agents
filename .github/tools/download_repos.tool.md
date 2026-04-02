
---
description: Tool for cloning multiple git repositories listed in a workspace `.env` or provided via environment variables using `download_repos.py`.
entrypoint: download_repos.py:main
name: download_repos_tool
inputs:
  - name: env
    type: string
    description: Path to the `.env` file to read (relative to the workspace root). If omitted, the tool will use the default workspace `.env`.
  - name: dest
    type: string
    description: Destination folder name under the workspace root where repos will be cloned (default: `temp`).
outputs:
  - name: result
    type: string
    description: Status messages from the cloning process or an error description.
---

This tool invokes the `main()` function from `download_repos.py`. It reads a `REPOS` variable (a comma-separated list of HTTPS repo URLs) from the provided `.env` file or from environment variables, then clones or updates each repository into the destination folder under the workspace root. Use `env` to point to a specific `.env` file (e.g., `.env`), and `dest` to change the clone target directory name (e.g., `repos`).

Examples:

- Use the workspace `.env` and default destination `temp`.

- Provide a custom `.env` path: `--env .env`
- Change destination folder: `--dest repos`

The tool returns a `result` string summarizing actions taken and any errors encountered.
