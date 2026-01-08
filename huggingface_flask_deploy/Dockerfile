FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip list

# Pre-download YOLOv8 model during build
RUN python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('✓ Model downloaded successfully!')"

# Copy application
COPY app.py .

# Expose port
EXPOSE 7860

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Run the application
CMD ["python", "app.py"]

