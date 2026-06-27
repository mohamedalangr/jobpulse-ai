FROM python:3.11-slim

LABEL org.opencontainers.image.title="JobPulse AI Migration Worker"
LABEL org.opencontainers.image.description="Executes Alembic migrations during deployment."

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY migrations/ migrations/
COPY src/ src/

# Run migrations automatically
CMD ["alembic", "upgrade", "head"]
