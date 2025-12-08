#!/bin/bash

# Start Frontend Script for Smart Waste Sorter
# This script starts the React development server

echo "=========================================="
echo "🎨 Starting Smart Waste Sorter Frontend"
echo "=========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

# Navigate to frontend directory
cd smart-sorter-ui

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "🎯 Starting React development server..."
echo "   App will open at http://localhost:3000"
echo "   Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Start the React application
npm start



