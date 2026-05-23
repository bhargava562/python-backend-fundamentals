# ================================================
# STAGE 1: Build Environment (Compiler stage)
# ================================================
FROM python:3.12-slim AS build-environment

WORKDIR /dependencies-build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ================================================
# STAGE 2: Runtime Environment (Optimized)
# ================================================
FROM python:3.12-slim AS production-runtime

LABEL maintainer="Zenovox Development Team"
LABEL description="Production-ready FastAPI backend system"

WORKDIR /deployment/app

# Install runtime dependencies only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy built Python packages from build stage
COPY --from=build-environment /root/.local /root/.local

# Copy application source code
COPY . .

# Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random

# Security: Create non-root user to run application
RUN useradd -u 8888 -m apprunner && \
    chown -R apprunner:apprunner /deployment

# Switch to non-root user
USER apprunner

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
