# Official cloud plugins (recommend; install only with approval)

| Provider | Claude Code install | Notes |
|---|---|---|
| Azure | `/plugin marketplace add microsoft/azure-skills` then `/plugin install azure@azure-skills` | Includes Azure MCP server; sends telemetry via hooks. Check policy before installing. |
| AWS | `/plugin install aws-core@claude-plugins-official`; deploy/serverless: `/plugin marketplace add awslabs/agent-plugins` | Remote AWS MCP server via proxy. |
| Google Cloud | `claude plugin marketplace add google/skills` then `claude plugin install <plugin>@google-plugins` | |
| Terraform | `claude plugin marketplace add hashicorp/agent-skills` then `claude plugin install terraform@hashicorp` | Use alongside any cloud. |

Before recommending, confirm the plugin is allowed under `context/TEAM.md` → Hard rules (some orgs restrict third-party plugins or telemetry).
Cloud plugins give the agent credentials-backed tools. Never run anything that changes cloud resources without `ship-to-production` approval.
