---
name: visualize-codebase
description: Produce a visual onboarding guide to a codebase (architecture diagram, module map, key request flows, data model and hotspot map) as a single HTML page. Use when joining a new project, when the user asks to "show me" or "visualize" the codebase, or after map-codebase.
---

# Visualize the codebase

The user is a visual learner. Show structure with pictures first and keep text to captions. Output: `docs/visual/codebase.html`, a single self-contained file. If the Artifact tool is available, publish it there too.

## Build these views (skip any that don't apply)

1. **System context:** Mermaid `flowchart`: users, this system, external systems (DBs, queues, APIs, cloud services) from `docs/environment.md`.
2. **Module map:** Mermaid `flowchart` of top-level modules/packages and their dependencies (from imports). Size or annotate by lines of code; colour test coverage: green = tested, amber = partly, red = none.
3. **Key flows:** 2–3 Mermaid `sequenceDiagram`s for the most important paths (e.g. main API request, nightly job), traced from entry point through the code.
4. **Data model:** Mermaid `erDiagram` from ORM models, migrations or schema files.
5. **Hotspots:** the treemap from `scripts/change-map.py --since "1 year ago" --hotspots` (files sized by size, coloured by how often they change). Big + hot = risky.
6. **Reading tour:** an ordered list "read these 7 files first", each with one sentence on why.

## Rules
- Every box must map to real code: include the path in the node label or tooltip. Don't invent components.
- Keep each diagram under ~25 nodes; split by area if larger.
- Mark anything inferred as *(unverified)*.
- Load Mermaid from `https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js`.
