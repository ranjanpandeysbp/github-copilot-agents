---
name: pr_review
description: Skill to perform an automated PR/code review of repositories located in the `temp/` folder. Checks SOLID, design patterns, microservices architecture, OWASP Top 10, clean code, and sustainability.
entrypoint: pr_review:run
---

This skill inspects code downloaded into the workspace `temp/` folder and generates a structured markdown report for each repository/PR.

Behavior:
- Walk the `temp/` folder at repo root and discover repositories.
- For each repo, analyze modified files (as produced by the download step) and search for issues related to:
  - SOLID principles violations
  - Missing or misused design patterns
  - Microservices anti-patterns (tight coupling, shared DBs, sync-heavy comms)
  - Security issues based on OWASP Top 10 (injection, auth, sensitive data exposure, etc.)
  - Clean code issues (naming, duplication, long methods, complex conditionals)
  - Sustainability (test coverage gaps, large methods, hard-to-change code)
- Produce a markdown report in the `reports/` folder (created at the workspace root next to `.github/`) for each repo with filename: `{repo_name}_comprehensive_review_{YYYYMMDD_HHMMSS}.md`.
- Each run creates a new timestamped report to preserve analysis history without overwriting previous reports.

Report format (per issue):

- **File:** path/to/file.java
- **Line:** line_number
- **Severity:** Critical / High / Medium / Low
- **Issue:** Short description
- **Code:** Inline code snippet causing the issue (3-6 lines)
- **Recommendation:** Suggested fix

Implementation:
- Analyzes all Java files in repositories located in the `temp/` folder
- Groups issues by severity for better readability
- Includes detailed recommendations for each identified issue

Notes:
- Timestamped reports enable tracking of changes across multiple review runs
- Each execution generates a new report file with current timestamp
- Previous reports are preserved for historical comparison
