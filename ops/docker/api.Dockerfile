# Builder Stage: Install dependencies and build wheels
FROM python:3.11-slim as builder

LABEL org.opencontainers.image.title="JobPulse AI API Builder"

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Build wheels for faster and smaller runtime installation
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Runtime Stage: Lean image running the application
FROM python:3.11-slim as runtime

LABEL org.opencontainers.image.title="JobPulse AI API"
LABEL org.opencontainers.image.version="0.5.0"
LABEL org.opencontainers.image.source="https://github.com/jobpulse-ai"
LABEL org.opencontainers.image.description="FastAPI backend for Semantic Search and Career Intelligence"

# Create non-root user
RUN useradd -m -s /bin/bash appuser

WORKDIR /app

# Install runtime dependencies using the builder's wheels
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the actual application
COPY src/ /app/src/
COPY config/ /app/config/

# Fix permissions
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# We use shell form to expand env variables if needed, though Uvicorn args are safer
CMD ["uvicorn", "src.api.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
