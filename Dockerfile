# Multi-stage Docker build
FROM node:18-alpine AS frontend-build

WORKDIR /frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build React app
RUN npm run build

# Backend + Nginx stage
FROM python:3.11-slim

# Install nginx and system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for backend
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend from previous stage
COPY --from=frontend-build /frontend/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Create startup script
RUN echo '#!/bin/bash\n\
nginx\n\
uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /start.sh && chmod +x /start.sh

# Start services
CMD ["/start.sh"]
