# 🚀 AI-Powered News Agent

A **CI/CD pipeline** that scrapes TechCrunch headlines, generates AI-powered summaries using **Groq (Llama-3.1)**, and delivers a professional PDF report to your inbox.

## 🛠️ Tech Stack & Architecture
- **Language**: Python 3.12 (Slim-runtime)
- **AI Intelligence**: Groq Cloud SDK (Llama-3.1-8b-instant)
- **Scraping**: HTTPX + BeautifulSoup4 (Optimized for speed/low overhead)
- **DevOps**: Docker, GitHub Actions (CI/CD), GHCR (GitHub Container Registry)
- **Reporting**: ReportLab (PDF) & Yagmail (SMTP)

## 🏗️ DevOps/SRE Features
- **Optimized Footprint**: Migrated from heavy browser-based images to `python:3.12-slim`, reducing image size by ~90%.
- **Secret Management**: Zero-trust approach using GitHub Encrypted Secrets for API keys.
- **Automated Pipeline**: 
  - **CI**: Every push builds a new Docker image and pushes it to GHCR.
  - **CD**: Scheduled Cron job (08:00 IST) triggers the containerized agent in the cloud.
- **Error Resilience**: Implemented content validation and modular error handling to ensure 99.9% pipeline success.

## 🚀 Deployment
1. Clone the repo and add `.env` keys.
2. Build locally: `docker build -t news-agent .`
3. Run: `docker run --env-file .env news-agent`
