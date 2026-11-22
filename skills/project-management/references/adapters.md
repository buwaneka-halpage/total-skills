# PM tool adapters

All writes are draft-first. Read-only commands may run freely.

## Detection (record result in docs/environment.md → Project management)
- `gh project list --owner <org>` returns projects linked to the repo → GitHub Projects
- Issue/PR text or branch names with keys like `ABC-123` → Jira; `AB#123` → Azure Boards; `ENG-123` with linear.app links → Linear
- Links in README/CONTRIBUTING: `atlassian.net`, `dev.azure.com`, `linear.app`, `app.asana.com`, `notion.so`, `monday.com`, `smartsheet.com`
- MCP connectors available in the session (Atlassian, Linear, Asana, Notion, Azure DevOps)
- Otherwise: ask the user.

## GitHub Projects (default)
Needs: `gh auth refresh -s project` (project scope).
```bash
gh project create --owner <org> --title "<project>"                       # draft-first
gh project field-create <num> --owner <org> --name "Start date" --data-type DATE
gh project field-create <num> --owner <org> --name "Target date" --data-type DATE
gh project field-create <num> --owner <org> --name "Estimate (days)" --data-type NUMBER
gh project field-create <num> --owner <org> --name "Phase" --data-type SINGLE_SELECT --single-select-options "Foundation,Build,Verify,Release"
gh project item-add <num> --owner <org> --url <issue-url>
gh project field-list <num> --owner <org> --format json                  # get field + option IDs
gh project item-edit --project-id <PID> --id <ITEM_ID> --field-id <FID> --date 2026-11-18
gh project item-list <num> --owner <org> --format json                   # read for tracking
```
Dependencies: GitHub issue "blocked by" relationships where enabled; otherwise `Blocked by #n` in the issue body.
Gantt in GitHub's UI: the project's **Roadmap** layout (set Start/Target date fields as the date range). Layout views are set in the UI; tell the user how.
Milestones (`gh api repos/{o}/{r}/milestones`) can carry phases with due dates.

## Jira (Atlassian)
Tooling: the Atlassian Rovo MCP connector (claude.ai connectors) or Jira REST via `curl` with an API token from the environment.
Mapping: Task → Story/Task, Phase → Epic, dates → `Start date` / `Due date`, Depends → issue link "blocks".
Gantt in Jira: Timeline (per project) or Plans (Advanced Roadmaps, Premium).
Export for gantt.py: JQL search → JSON → map fields → `--json`.

## Azure Boards (Azure DevOps)
Tooling: `az boards` (Azure CLI + `azure-devops` extension) or Microsoft's Azure DevOps MCP server.
```bash
az boards work-item create --type "Task" --title "…" --fields "Microsoft.VSTS.Scheduling.StartDate=2026-11-18" "Microsoft.VSTS.Scheduling.TargetDate=2026-11-20"
az boards work-item relation add --id <id> --relation-type "Predecessor" --target-id <dep>
az boards query --wiql "SELECT … FROM WorkItems WHERE …" -o json         # read for tracking
```
Mapping: Phase → Feature/Epic or Iteration path. Gantt: Delivery Plans (or a Marketplace Gantt extension).

## Linear
Tooling: Linear MCP connector. Mapping: Phase → Project milestone, dates → Project/Cycle dates, Depends → "blocked by" relation. Timeline view in Linear projects.

## Asana
Tooling: Asana MCP connector. Mapping: Phase → Section, dates → start/due, Depends → task dependencies. Gantt: Timeline / Gantt view.

## Notion
Tooling: Notion MCP connector. A database with Date (range), Status, Phase (select), Depends (relation) properties. Gantt: Timeline view.

## MS Project, Smartsheet, monday.com, Excel, or anything else
Export the schedule from gantt.py's JSON as CSV (`id,title,phase,start,end,days,depends,owner,status`). Every one of these imports CSV.
Read status back from their CSV/XLSX export → `--json`. Don't scrape web UIs.

## JSON format for gantt.py --json
`[{"id":"T1","title":"…","phase":"Build","start":"2026-11-18","end":"2026-11-20","days":3,"depends":["T0"],"status":"in progress","owner":"…","issue":"42"}]`
`start`/`end` are optional. Missing dates are scheduled from dependencies and `days`.
