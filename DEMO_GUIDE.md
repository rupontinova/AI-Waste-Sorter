# 🎬 Demo Guide: Smart Waste Sorter

## Visual Walkthrough

This guide shows you exactly what to expect when running the Smart Waste Sorter application.

## 🚀 Starting the Application

### Step 1: Start Backend

When you run `./start_backend.sh` or `python3 app.py`, you'll see:

```
============================================================
Initializing Smart Waste Sorter Backend
============================================================
✓ Model loaded successfully!
  Model classes: 80
============================================================

============================================================
🚀 Starting Flask Backend Server
============================================================
Server will run on: http://localhost:5001
API Endpoints:
  GET  / - Health check
  POST /predict - Image classification
  GET  /categories - Available waste categories
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in production.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.1.xxx:5001
```

✅ **Backend is ready when you see "Running on http://127.0.0.1:5001"**

### Step 2: Start Frontend

When you run `./start_frontend.sh` or `npm start`, you'll see:

```
Compiled successfully!

You can now view smart-sorter-ui in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.xxx:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

✅ **Your browser will automatically open to http://localhost:3000**

## 🖥️ What You'll See in the Browser

### Initial Screen

```
┌─────────────────────────────────────────────────────────┐
│          🗑️ Smart Waste Sorter                          │
│     AI-Powered Waste Classification System              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [📁 Choose Image]  [file_name.jpg]                      │
│                                                           │
│  [🔍 Classify Waste]  [🗑️ Clear]                         │
│                                                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│                  How to Use                               │
│  1. Click "Choose Image" to select a photo...            │
│  2. Click "Classify Waste" to analyze...                 │
│  3. View the detected items and their categories         │
│                                                           │
│              Waste Categories                             │
│  🔴 Plastic   🟢 Paper   🔵 Metal   🟠 Organic           │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### After Uploading and Analyzing an Image

```
┌─────────────────────────────────────────────────────────┐
│          🗑️ Smart Waste Sorter                          │
│     AI-Powered Waste Classification System              │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [📁 Choose Image]  waste_photo.jpg                      │
│                                                           │
│  [🔍 Classify Waste]  [🗑️ Clear]                         │
│                                                           │
├──────────────────────────┬──────────────────────────────┤
│                          │                               │
│   Detection Results      │  Waste Category Counts        │
│                          │                               │
│  ┌────────────────────┐ │  🔴 Plastic: 2                │
│  │                    │ │  🟠 Organic: 3                │
│  │  [Image with red   │ │  🟢 Paper: 1                  │
│  │   boxes around     │ │                               │
│  │   bottles labeled  │ │  Total Objects Detected: 6    │
│  │   "Plastic: bottle"│ │                               │
│  │   and green boxes  │ │                               │
│  │   around food]     │ │                               │
│  │                    │ │                               │
│  └────────────────────┘ │                               │
│                          │                               │
└──────────────────────────┴──────────────────────────────┘
```

## 🎯 Testing with Sample Images

### Good Test Images

Images that work well:
- ✅ **Kitchen photos** with bottles, food, utensils
- ✅ **Desk photos** with books, pens, coffee cups
- ✅ **Grocery items** - fruits, vegetables, packaged goods
- ✅ **Recycling bin contents**

### Example Detection Scenarios

#### Scenario 1: Water Bottle
```
Input: Photo of a plastic water bottle
Detection: 
  - Original: "bottle" 
  - Category: Plastic
  - Confidence: 87%
  - Box: Red rectangle around bottle
```

#### Scenario 2: Apple
```
Input: Photo of an apple
Detection:
  - Original: "apple"
  - Category: Organic
  - Confidence: 92%
  - Box: Orange rectangle around apple
```

#### Scenario 3: Book
```
Input: Photo of a book
Detection:
  - Original: "book"
  - Category: Paper
  - Confidence: 85%
  - Box: Green rectangle around book
```

#### Scenario 4: Mixed Items
```
Input: Photo with bottle, apple, book, and scissors
Detections:
  1. bottle → Plastic (87%)
  2. apple → Organic (92%)
  3. book → Paper (85%)
  4. scissors → Metal (78%)

Category Counts:
  Plastic: 1
  Organic: 1
  Paper: 1
  Metal: 1
```

## 🎨 Color Coding Guide

When you see bounding boxes:

- **🔴 Red boxes** = Plastic items
- **🟢 Green boxes** = Paper items
- **🔵 Blue boxes** = Metal items
- **🟠 Orange boxes** = Organic/Food items
- **⚫ Gray boxes** = Other/Unknown items

## 📊 Understanding the Results

### Confidence Score
- **> 80%** = Very confident (most likely correct)
- **60-80%** = Moderately confident
- **< 60%** = Low confidence (may need verification)

The system filters out detections below 25% confidence.

### Category Counts
Shows how many items of each type were detected:

```
Plastic: 3    ← 3 plastic items found
Paper: 1      ← 1 paper item found
Metal: 2      ← 2 metal items found
Organic: 5    ← 5 organic items found
```

### Total Objects
Sum of all detected items across all categories.

## 🧪 Testing the Backend Manually

### Test 1: Health Check
```bash
curl http://localhost:5001/
```

Expected output:
```json
{
  "status": "online",
  "service": "Smart Waste Sorter API",
  "version": "1.0.0",
  "model": "YOLOv8n",
  "categories": ["Plastic", "Paper", "Metal", "Organic"]
}
```

### Test 2: Get Categories
```bash
curl http://localhost:5001/categories
```

Expected output:
```json
{
  "categories": ["Plastic", "Paper", "Metal", "Organic", "Other"],
  "description": {
    "Plastic": "Plastic bottles, containers, bags, and packaging",
    "Paper": "Paper, cardboard, newspapers, magazines",
    "Metal": "Aluminum cans, metal containers, foil",
    "Organic": "Food waste, fruits, vegetables, biodegradable items"
  }
}
```

### Test 3: Upload an Image
```bash
curl -X POST -F "image=@test_image.jpg" http://localhost:5001/predict
```

Expected output:
```json
{
  "success": true,
  "detections": [
    {
      "box": [150.5, 200.3, 350.8, 450.2],
      "label": "Plastic",
      "originalLabel": "bottle",
      "confidence": 0.87
    }
  ],
  "counts": {
    "Plastic": 1
  },
  "total_objects": 1
}
```

## 🐛 What to Do If...

### ❌ Nothing happens when clicking "Classify Waste"

**Check:**
1. Is the Flask backend running? (Look for "Running on http://127.0.0.1:5001")
2. Open browser console (F12) - any error messages?
3. Try refreshing the page

### ❌ See "Cannot connect to backend" message

**Solution:**
```bash
# Check if backend is running
curl http://localhost:5001/

# If not responding, restart it
cd /Users/nova/Documents/swi-prolog/AI_LAB/waste_sorter
python3 app.py
```

### ❌ No objects detected in image

**Possible reasons:**
1. Image contains objects not in COCO dataset (80 classes)
2. Objects too small or obscured
3. Low confidence (< 25% threshold)

**Try:**
- Use clearer, higher quality images
- Ensure good lighting
- Take photos from different angles

### ❌ Wrong category assigned

**Why this happens:**
The base YOLOv8n model detects generic objects. The class mapping might not be perfect.

**Solution:**
Fine-tune the model on actual waste images or adjust mappings in `app.py`

## 🎓 Learning Exercises

### Exercise 1: Test Different Objects
Try uploading photos of:
- 📱 Your workspace
- 🍕 Your lunch
- 📚 Your bookshelf
- ♻️ Your recycling bin

See what gets detected!

### Exercise 2: Modify Colors
1. Open `smart-sorter-ui/src/App.js`
2. Find `categoryColors` (around line 10)
3. Change the hex colors
4. Save and see it update in browser!

### Exercise 3: Adjust Confidence
1. Open `app.py`
2. Find `conf=0.25` (around line 155)
3. Change to `conf=0.50` for stricter detection
4. Restart backend and test

### Exercise 4: Add Your Own Mapping
1. Open `app.py`
2. Find `CLASS_MAP` dictionary
3. Add new mappings like `'laptop': 'Other'`
4. Test with an image of a laptop

## 📈 Next Steps

Now that you've seen it work:

1. ✅ Read the full [README.md](README.md) for technical details
2. ✅ Try [QUICKSTART.md](QUICKSTART.md) for different setup options
3. ✅ Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture
4. ✅ Experiment with your own images
5. ✅ Consider fine-tuning on real waste data

## 🎉 Congratulations!

You now have a fully functional AI-powered waste classification system!

---

**Happy Testing! 🗑️♻️**



