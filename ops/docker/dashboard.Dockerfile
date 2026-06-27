FROM python:3.11-slim

LABEL org.opencontainers.image.title="JobPulse AI Dashboard"
LABEL org.opencontainers.image.description="Streamlit Reference Client"

WORKDIR /app

# Only install what the frontend needs
RUN pip install --no-cache-dir streamlit requests plotly pydantic pydantic-settings

COPY .streamlit/ .streamlit/
COPY config/dashboard.yaml config/
COPY src/dashboard/ src/dashboard/

EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
