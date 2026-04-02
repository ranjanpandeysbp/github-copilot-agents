---
name: doc_generator
description: Skill to analyze Java code repositories and generate comprehensive technical documentation including design diagrams and code walkthroughs.
entrypoint: doc_generator:run
---

This skill inspects code downloaded into the workspace `temp/` folder and generates comprehensive technical documentation for each repository.

Behavior:
- Walk the `temp/` folder at repo root and discover repositories.
- For each repo, analyze the codebase structure, components, and architecture, then generate comprehensive documentation including:
  - **Data Flow Diagram** (Mermaid): Illustrating how data flows through the system
  - **Interaction Diagrams** (Mermaid): Showing component interactions and dependencies
  - **Sequence Diagrams** (Mermaid): Depicting key business process flows
  - **Class Diagrams** (Mermaid): Representing the class hierarchy and relationships
  - **Entity Relationship Diagrams** (Mermaid): Showing database schema and relationships
  - **Code Walkthrough** (Detailed markdown): Step-by-step explanation of key components, patterns used, and architectural decisions
  - **Tech Stack Summary**: Technologies, frameworks, and libraries used
  - **Architecture Overview**: High-level system design and component responsibilities
  - **Key Findings and Observations**: Important patterns, best practices, and potential improvements

- Produce a markdown report in the `docs_report/` folder (created at the workspace root) for each repo with filename: `{repo_name}_{YYYYMMDD_HHMMSS}.md`.
- Each run creates a new timestamped report to preserve documentation history without overwriting previous reports.

Report format structure:

1. **Repository Overview**
   - Repository name and description
   - Tech stack and framework information

2. **System Architecture**
   - Data Flow Diagram
   - Component Interaction Diagram
   - Architecture Overview

3. **Detailed Component Analysis**
   - Database Schema (ER Diagram)
   - Key Classes and Services (Class Diagram)
   - Important Business Flows (Sequence Diagrams)

4. **Code Walkthrough**
   - Module-by-module explanation
   - Key design patterns identified
   - Important algorithms and logic

5. **Summary and Best Practices**
   - Technology choices rationale
   - Design decisions
   - Recommended improvements

Implementation:
- Analyzes all Java files in repositories located in the `temp/` folder
- Generates Mermaid diagrams based on actual code structure
- Creates detailed, beginner-friendly documentation
- Groups information by component for better readability

Notes:
- Timestamped reports enable tracking of documentation across multiple generations
- Each execution generates a new report file with current timestamp
- Previous reports are preserved for historical comparison
- Focus on clarity and usefulness for both beginners and experienced developers
