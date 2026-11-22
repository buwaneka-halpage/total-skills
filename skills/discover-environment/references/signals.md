# Detection signals

| Signal (file / content) | Means |
|---|---|
| `azure.yaml`, `*.bicep`, `azuredeploy.json`, `azure-pipelines.yml`, `.azure/`, `host.json`+`local.settings.json` (Functions), `@azure/*` / `azure-*` SDK deps, `provider "azurerm"` | Azure |
| `cdk.json`, `template.yaml`/`samconfig.toml` (SAM), `serverless.yml`, `buildspec.yml`, `appspec.yml`, `.ebextensions/`, `aws-sdk`/`boto3`/`@aws-sdk/*` deps, `provider "aws"` | AWS |
| `app.yaml` (App Engine), `cloudbuild.yaml`, `skaffold.yaml`, `.gcloudignore`, `google-cloud-*`/`@google-cloud/*` deps, `provider "google"` | Google Cloud |
| `*.tf`, `.terraform.lock.hcl` | Terraform (provider blocks name the cloud) |
| `Pulumi.yaml` | Pulumi (check runtime deps for cloud) |
| `Dockerfile`, `docker-compose*.yml` | Containers |
| `k8s/`, `helm/`, `Chart.yaml`, `kustomization.yaml` | Kubernetes (check context: AKS/EKS/GKE/on-prem) |
| `.github/workflows/*.yml` | GitHub Actions |
| `azure-pipelines.yml` | Azure Pipelines |
| `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/` | GitLab CI, Jenkins, CircleCI |
| `.github/dependabot.yml`, `renovate.json` | Automated dependency updates |
| Workflow steps `azure/login`, `aws-actions/configure-aws-credentials`, `google-github-actions/auth` | Deploys to that cloud |
| No cloud signal, but `systemd`/`ansible`/VM scripts | On-premises (ask the user) |
