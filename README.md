[![Build and Push Docker Image](https://github.com/amargmail/aischeduler/actions/workflows/build-image.yml/badge.svg)](https://github.com/amargmail/aischeduler/actions/workflows/build-image.yml)
[![Daily AI News Report](https://github.com/amargmail/aischeduler/actions/workflows/daily-report.yml/badge.svg)](https://github.com/amargmail/aischeduler/actions/workflows/daily-report.yml)
[![Terraform Check](https://github.com/amargmail/aischeduler/actions/workflows/terraform-check.yml/badge.svg)](https://github.com/amargmail/aischeduler/actions/workflows/terraform-check.yml)
# 🚀 AI-Powered News Agent

A **CI/CD pipeline** that scrapes TechCrunch headlines, generates AI-powered summaries using **Groq (Llama-3.1)**, and delivers a PDF report to your inbox.

## 🛠️ Tech Stack & Architecture
- **Engine**: Python 3.12 (Modular Source Layout)
- **Scraping**: Lightweight `httpx` + `BeautifulSoup4` (Optimized for speed/low overhead)
- **AI Intelligence**: Groq Cloud SDK (Llama-3.1-8b-instant) for sub-second summarization.
- **Reporting**: Automated PDF generation via `ReportLab` and SMTP delivery via `Yagmail`.

## 🏗️ Features
### 1. Resource Optimization (Multi-stage Docker)
- **Optimized Footprint**
Reduced the Docker image footprint from **2GB (Playwright-based) to 190MB (Python-Slim)**. 
- Utilized **Multi-stage builds** to separate the build-time dependencies (gcc, python-dev) from the runtime environment.
- Result: 90% reduction in storage costs and significantly faster CI/CD deployment cycles.
- **Secret Management**: Zero-trust approach using GitHub Encrypted Secrets for API keys.
- **Automated Pipeline**: 
  - **CI**: Every push builds a new Docker image and pushes it to GHCR.
  - **CD**: Scheduled Cron job (08:00 IST) triggers the containerized agent in the cloud.
  - **Error Resilience**: Implemented content validation and modular error handling to ensure 99.9% pipeline success.

### 2. Infrastructure as Code (Terraform)
Implemented **Terraform** to manage the GitHub repository as a "Managed Resource."
- **State Management**: Performed a `terraform import` of existing manual infrastructure into a declarative state.
- **Drift Detection**: Automated GitOps workflow to identify and correct manual configuration changes in the GitHub UI.

### 3. CI/CD Pipeline (GitHub Actions)
- **Shift-Left Testing**: Integrated `Pytest` with `Mocks` as a mandatory gatekeeper. The Docker build fails automatically if unit tests do not pass.
- **Automated Registry**: Verified images are pushed to **GHCR (GitHub Container Registry)** using secure, short-lived tokens.
- **Future-Proofing**: Proactively migrated all Action runners to **Node.js 24** to stay ahead of the 2026 deprecation roadmap.

### 4. Observability & Security
- **Active Monitoring**: Integrated a **Dead Man's Snitch** heartbeat via `Healthchecks.io` to detect silent failures in Cron-scheduled jobs.
- **Secret Management**: Zero-trust approach using GitHub Encrypted Secrets; no keys are stored in the source code or image layers.

## 🚀 Getting Started
1. **Clone & Setup**:
   ```bash
   git clone https://github.com
   pip install -r requirements.txt
  ```
2. **Infrastructure**
  ```bash
   cd terraform
   terraform init
   terraform apply -var="groq_api_key=your_key"
  ```
3. **Run Locally**
```bash
   python3 main.py
```
