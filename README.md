# 🗑️ Smart Waste Sorter

An AI-powered waste classification system built with YOLOv8, Flask, and React.

**Academic Project:** 4th Year, 1st Semester - Artificial Intelligence Lab

## 🌐 Live Demo

🚀 **Try it now:** [https://ai-waste-sorter.vercel.app/](https://ai-waste-sorter.vercel.app/)

## 📋 Overview

The Smart Waste Sorter is an end-to-end computer vision application that uses YOLOv8 object detection to identify and classify waste items into four categories:

- 🔴 **Plastic** - Bottles, containers, bags, packaging
- 🟢 **Paper** - Paper, cardboard, newspapers, magazines  
- 🔵 **Metal** - Cans, metal containers, aluminum foil
- 🟠 **Organic** - Food waste, fruits, vegetables

## 📸 Application Preview

![Smart Waste Sorter Application](resources/ss_smart_waste_fullpage.png)

## 🏗️ Architecture

```
┌─────────────────┐      HTTP Request      ┌──────────────────┐
│  React Frontend │ ───────────────────────> │  Flask Backend   │
│  (Port 3000)    │                          │  (Port 5000)     │
│                 │ <─────────────────────── │                  │
│  - File Upload  │      JSON Response       │  - YOLOv8 Model  │
│  - Visualization│                          │  - Inference     │
│  - Results      │                          │  - Class Mapping │
└─────────────────┘                          └──────────────────┘
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+ 
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Download and verify the AI model:**
```bash
python3 load_model.py
```

This will download the YOLOv8 model (first run only) and verify it's working.

3. **Start the Flask backend:**
```bash
python3 app.py
```

The backend will be available at `http://localhost:5001`

**Note:** We use port 5001 instead of 5000 because macOS uses port 5000 for AirPlay/AirTunes.

### Frontend Setup

1. **Navigate to the React app directory:**
```bash
cd smart-sorter-ui
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

The app will open automatically at `http://localhost:3000`

## 📖 Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Click "Choose Image"** and select a photo containing waste items

3. **Click "Classify Waste"** to analyze the image

4. **View results:**
   - Bounding boxes around detected objects (color-coded by category)
   - Category counts showing the distribution of waste types
   - Original object labels with confidence scores

## 🧠 How It Works

### 1. Model Loading (`load_model.py`)

- Attempts to load a waste-specific YOLOv8 model from Hugging Face
- Falls back to the base YOLOv8n model for demonstration
- Downloads model weights automatically on first run

### 2. Backend API (`app.py`)

The Flask backend provides three endpoints:

- `GET /` - Health check and API information
- `POST /predict` - Main classification endpoint
  - Accepts: multipart/form-data with 'image' field
  - Returns: JSON with detections, bounding boxes, and counts
- `GET /categories` - Returns available waste categories

**Class Remapping Logic:**

The backend intelligently maps the 80 COCO object classes to 4 waste categories:

```python
# Example mappings:
'bottle' → 'Plastic'
'apple' → 'Organic'  
'book' → 'Paper'
'scissors' → 'Metal'
```

For objects not in the predefined map, heuristic keyword matching is used.

### 3. Frontend UI (`smart-sorter-ui/`)

React application features:

- **File Upload**: Drag-and-drop or click to select images
- **Canvas Visualization**: Draws bounding boxes and labels on detected objects
- **Results Display**: Shows category counts and statistics
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
waste_sorter/
├── app.py                    # Flask backend API
├── load_model.py             # Model loading script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── yolov8n.pt               # Downloaded YOLOv8 model (auto-created)
└── smart-sorter-ui/         # React frontend
    ├── src/
    │   ├── App.js           # Main React component
    │   ├── App.css          # Styling
    │   └── index.js         # Entry point
    ├── public/
    └── package.json         # Node dependencies
```

## 🔧 Configuration

### Backend Configuration

Edit `app.py` to customize:

- **Model path**: Change `YOLO('yolov8n.pt')` to use a different model
- **Confidence threshold**: Adjust `conf=0.25` in the predict function
- **Class mappings**: Modify the `CLASS_MAP` dictionary
- **Port**: Change `port=5000` in `app.run()`

### Frontend Configuration

Edit `src/App.js` to customize:

- **API endpoint**: Change `http://localhost:5000` if backend is on a different host
- **Colors**: Modify `categoryColors` object
- **Timeout**: Adjust `timeout: 30000` for slower networks

## 🎯 Advanced Usage

### Fine-Tuning the Model

To train on custom waste data:

1. Prepare a dataset in YOLO format (images + labels)
2. Create a `data.yaml` configuration file
3. Run training:

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='data.yaml', epochs=50, imgsz=640)
```

4. Replace `yolov8n.pt` in `app.py` with your trained `best.pt`

### Deployment

**Backend (Flask):**
- Use a production WSGI server like Gunicorn
- Deploy to cloud platforms (Google Cloud Run, AWS, Heroku)
- Enable HTTPS and configure CORS properly

**Frontend (React):**
- Run `npm run build` to create production build
- Deploy to Netlify, Vercel, or any static hosting
- Update API endpoint to production backend URL

## 🧪 Testing

### Test the Backend Independently

```bash
curl -X POST -F "image=@test_image.jpg" http://localhost:5001/predict
```

### Check Backend Status

```bash
curl http://localhost:5001/
```

### Run Automated Tests

```bash
python3 test_backend.py
```

Expected response:
```json
{
  "status": "online",
  "service": "Smart Waste Sorter API",
  "version": "1.0.0",
  "model": "YOLOv8n",
  "categories": ["Plastic", "Paper", "Metal", "Organic"]
}
```

## 📊 API Reference

### POST /predict

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `image` field with image file

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "box": [x1, y1, x2, y2],
      "label": "Plastic",
      "originalLabel": "bottle",
      "confidence": 0.87
    }
  ],
  "counts": {
    "Plastic": 2,
    "Organic": 1
  },
  "total_objects": 3
}
```

## 🐛 Troubleshooting

### "Cannot connect to backend" error

- Ensure Flask backend is running (`python3 app.py`)
- Check that port 5001 is not blocked by firewall
- On macOS, port 5000 is used by AirPlay - we use port 5001 instead
- Verify the backend URL in `App.js` matches your setup (should be port 5001)

### Model download fails

- Check internet connection
- Try downloading manually from [Ultralytics releases](https://github.com/ultralytics/assets/releases)
- Place the model file in the project root

### CORS errors

- Ensure `flask-cors` is installed
- Check CORS configuration in `app.py`
- Try clearing browser cache

### Deployment Errors

#### Exit Status 127 (Command Not Found)
**Symptoms:** Deployment fails with "Exited with status 127"

**Causes:**
- Model file not available during deployment
- Missing build step to download the model
- Command path issues

**Solutions:**
1. Ensure `python load_model.py` is in your build command
2. Check that all dependencies are in `requirements.txt`
3. Verify gunicorn is installed (it is in requirements.txt)
4. See `DEPLOYMENT_FIX.md` for detailed fix instructions

**Fixed Configuration:**
```yaml
# render.yaml
buildCommand: pip install -r requirements.txt && python load_model.py
startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

```
# Procfile
web: python load_model.py && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

#### Timeout Errors
**Symptoms:** "Process failed to bind to port within 60 seconds"

**Solution:** Model loading takes time. Increase timeout:
```bash
gunicorn app:app --timeout 120
```

#### Out of Memory
**Symptoms:** Deployment crashes or restarts repeatedly

**Solution:** 
- YOLOv8 requires at least 512MB RAM
- Upgrade your hosting plan if needed
- Use `yolov8n.pt` (nano) instead of larger models

#### Disk Space Issues
**Symptoms:** "No space left on device"

**Solution:**
- Model files are ~6MB, ensure sufficient disk space
- Clear cache: `pip cache purge`
- Use persistent disk storage on Render

For detailed deployment troubleshooting, see **[DEPLOYMENT_FIX.md](DEPLOYMENT_FIX.md)**

## 🌐 Live Deployments

The application is deployed and accessible online:

### Frontend (React)
- **Live URL:** [https://ai-waste-sorter.vercel.app/](https://ai-waste-sorter.vercel.app/)
- **Platform:** Vercel
- **Features:** Custom React UI with image upload, real-time classification, and result visualization

### Backend (Flask API)
- **API URL:** `https://rupontinova-smart-waste-sorter-api.hf.space`
- **Platform:** Hugging Face Spaces
- **Specs:** 16GB RAM, Docker container
- **Endpoints:**
  - `GET /` - Health check
  - `POST /predict` - Image classification
  - `GET /categories` - Available categories

### Alternative Demo (Gradio UI)
- **Live URL:** [https://huggingface.co/spaces/rupontinova/smart-waste-sorter](https://huggingface.co/spaces/rupontinova/smart-waste-sorter)
- **Platform:** Hugging Face Spaces
- **Features:** Interactive Gradio interface with built-in UI

## 🙏 Technologies Used

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection model
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [React](https://react.dev/) - Frontend framework

---

Built with ❤️ using YOLOv8, Flask, and React

