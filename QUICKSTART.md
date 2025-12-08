# 🚀 Quick Start Guide - Smart Waste Sorter

Get up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher: `python3 --version`
- ✅ Node.js 14 or higher: `node --version`
- ✅ npm: `npm --version`

## Option 1: Using Startup Scripts (Recommended)

### Step 1: Start the Backend

Open a terminal and run:

```bash
cd /Users/nova/Documents/swi-prolog/AI_LAB/waste_sorter
./start_backend.sh
```

You should see:
```
✅ All checks passed!
🎯 Starting Flask server on http://localhost:5001
```

**Keep this terminal open!**

### Step 2: Start the Frontend

Open a **new** terminal and run:

```bash
cd /Users/nova/Documents/swi-prolog/AI_LAB/waste_sorter
./start_frontend.sh
```

The React app will automatically open in your browser at `http://localhost:3000`

## Option 2: Manual Setup

### Backend Setup

```bash
# Install dependencies
pip3 install -r requirements.txt --user

# Download the model (first time only)
python3 load_model.py

# Start the server
python3 app.py
```

### Frontend Setup

In a new terminal:

```bash
cd smart-sorter-ui

# Install dependencies (first time only)
npm install

# Start the development server
npm start
```

## Testing the System

### 1. Using the Web Interface

1. Open `http://localhost:3000` in your browser
2. Click "📁 Choose Image"
3. Select any image with common objects (bottles, food, books, etc.)
4. Click "🔍 Classify Waste"
5. View the results with bounding boxes and category counts!

### 2. Using curl (Command Line)

Test the backend directly:

```bash
# Health check
curl http://localhost:5001/

# Test prediction with an image
curl -X POST -F "image=@/path/to/your/image.jpg" http://localhost:5001/predict
```

### 3. Using the Test Script

```bash
python3 test_backend.py
```

Expected output: `3/3 tests passed 🎉`

## Common Issues & Solutions

### ❌ "Port 5001 already in use"

Kill the process using the port:
```bash
lsof -ti:5001 | xargs kill -9
```

### ❌ "Cannot connect to backend"

1. Verify Flask is running: `curl http://localhost:5001/`
2. Check the backend terminal for errors
3. Make sure you're using port 5001 (not 5000, which macOS uses for AirPlay)

### ❌ "Module not found" errors

Reinstall dependencies:
```bash
# Backend
pip3 install -r requirements.txt --user --force-reinstall

# Frontend
cd smart-sorter-ui && npm install
```

### ❌ Frontend shows "Cannot connect to backend"

1. Ensure Flask backend is running on port 5001
2. Check browser console (F12) for detailed error messages
3. Verify CORS is enabled in `app.py`

## What Objects Can It Detect?

The base YOLOv8n model can detect 80 common objects from the COCO dataset, including:

**Mapped to Plastic:**
- Bottles, cups, cell phones, keyboards, mice

**Mapped to Paper:**
- Books, newspapers

**Mapped to Metal:**
- Scissors, refrigerators, ovens

**Mapped to Organic:**
- Fruits (banana, apple, orange)
- Vegetables (broccoli, carrot)
- Food items (pizza, sandwich, hot dog)

## Next Steps

### Improve Accuracy with Fine-Tuning

To train on actual waste images:

1. Collect a dataset of waste photos (100+ images recommended)
2. Label them using [Roboflow](https://roboflow.com/)
3. Export in YOLOv8 format
4. Train the model:

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='waste_data.yaml', epochs=50)
```

5. Replace `yolov8n.pt` with your trained `best.pt` in `app.py`

### Deploy to Production

**Backend:**
- Containerize with Docker
- Deploy to Google Cloud Run, AWS, or Heroku
- Add authentication and rate limiting

**Frontend:**
- Build for production: `npm run build`
- Deploy to Netlify or Vercel
- Update API endpoint to production URL

### Add New Features

Ideas for enhancement:
- 📹 Real-time video stream processing
- 📱 Mobile app with React Native
- 🤖 IoT integration for smart bins
- 📊 Analytics dashboard for waste statistics
- 🌍 Multi-language support

## Support

For issues or questions:
1. Check the [README.md](README.md) for detailed documentation
2. Review error messages in terminal/browser console
3. Ensure all dependencies are correctly installed

---

**Happy Sorting! 🗑️♻️**



