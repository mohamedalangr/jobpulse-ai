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
docker compose up --build
```
*(Alternatively, simply run `bash ops/scripts/bootstrap.sh`)*

### 3. Accessing the Platform

Once the containers are running and the `migrate` worker finishes initializing the database, Nginx acts as the primary gateway:

- **Dashboard (Streamlit):** [http://localhost](http://localhost)
- **API Swagger Docs:** [http://localhost/api/docs](http://localhost/api/docs)
- **API Health Check:** [http://localhost/api/v1/health/live](http://localhost/api/v1/health/live)

> **Note**: On the first execution, the API container will download the HuggingFace embedding models. This takes a few minutes but will be securely cached in a persistent volume for all future restarts.

---

## Architecture Details
For a deep dive into the underlying systems, see:
- [System Components](docs/architecture/components.md)
- [Deployment Topology](docs/architecture/deployment.md)
