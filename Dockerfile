# Multi-stage Dockerfile for Smart Waste Sorter
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-build

WORKDIR /frontend
COPY smart-sorter-ui/package*.json ./
RUN npm ci --only=production
COPY smart-sorter-ui/ ./
RUN npm run build

# Stage 2: Backend with Python
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and model
COPY app.py .
COPY yolov8n.pt .

# Copy built frontend from stage 1
COPY --from=frontend-build /frontend/build /app/static

# Expose port
EXPOSE 5001

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=5001

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5001", "--workers", "2", "--timeout", "120"]

