# Use the official Python Slim image
#Stage 1: Build the application with all dependencies
FROM python:3.12-slim AS builder

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# WORKDIR /app
WORKDIR /build

# Install minimal system dependencies for PDF generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Create the final image with only the necessary files
FROM python:3.12-slim
WORKDIR /app
# Copy only the installed packages from the builder
COPY --from=builder /install /usr/local
COPY . .

RUN useradd -m appuser && chown -R appuser /app
USER appuser
# Run the app
CMD ["python", "main.py"]
