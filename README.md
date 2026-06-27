# JobPulse AI

An advanced system for analyzing career opportunities, evaluating candidate market fit, and building intelligent learning roadmaps using semantic search and feature engineering.

## 🚀 Quick Start (Docker Deployment)

JobPulse AI uses Docker Compose to run an entire production-grade stack locally with a single command. The stack includes a FastAPI backend, a Streamlit dashboard, a PostgreSQL database, and an Nginx reverse proxy.

### 1. Prerequisites
- Docker and Docker Compose installed
- Git

### 2. Startup

Clone the repository and run the bootstrap sequence:

```bash
git clone https://github.com/jobpulse-ai/jobpulse-ai.git
cd jobpulse-ai

# Copy environment variables
cp .env.example .env

# Spin up the infrastructure
# 3. Launch
docker compose up --build -d
```

Once running:
- **Dashboard**: `http://localhost:8501`
- **API Docs**: `http://localhost:8000/api/v1/docs`

> Note: To populate the database with initial market data, run:
> `docker compose exec api python ops/scripts/seed_database.py`

## 📖 Documentation
- [Architecture Details](docs/architecture/components.md)
- [Deployment Guide (VPS/Production)](docs/deployment.md)
- [Architecture Decision Records (ADRs)](docs/adr/)
