#!/usr/bin/env bash
set -e

echo "🚀 Bootstrapping JobPulse AI..."

# 1. Environment validation
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
fi

# 2. Start orchestration
echo "🐳 Starting Docker Compose (building images if necessary)..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

echo "✅ Bootstrapping complete. Services are starting up."
echo "Note: The API may take a few moments to become fully healthy as it preloads models and verifies the database."
echo ""
echo "Dashboard: http://localhost"
echo "API Docs: http://localhost/api/docs"
echo "API Health: http://localhost/api/v1/health/live"
