#!/bin/bash

# Start Backend Script for Smart Waste Sorter
# This script starts the Flask backend server

echo "=========================================="
echo "🚀 Starting Smart Waste Sorter Backend"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import flask, ultralytics, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Installing..."
    pip3 install -r requirements.txt --user
fi

# Check if model is downloaded
if [ ! -f "yolov8n.pt" ]; then
    echo "📥 Downloading YOLOv8 model..."
    python3 load_model.py
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "🎯 Starting Flask server on http://localhost:5001"
echo "   Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Start the Flask application
python3 app.py

