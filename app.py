"""
Flask Backend for Smart Waste Sorter
Provides AI-powered waste classification API with class remapping
"""

import io
import collections
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)

# Enable CORS for all routes, allowing the React frontend to make requests
CORS(app)

# --- Model Loading ---
print("="*60)
print("Initializing Smart Waste Sorter Backend")
print("="*60)

# Load the YOLOv8 model (will use the downloaded model)
import os
import sys

MODEL_PATH = 'yolov8n.pt'

# Check if model exists, if not try to download it
if not os.path.exists(MODEL_PATH):
    print("⚠️  Model file not found. Attempting to download...")
    try:
        # Try to download the model
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')  # This will auto-download
        print("✓ Model downloaded successfully!")
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        print("Please run 'python load_model.py' manually.")
        sys.exit(1)
else:
    model = YOLO(MODEL_PATH)
    print("✓ Model loaded successfully!")

print(f"  Model classes: {len(model.names)}")
print("="*60)

# --- Intelligent Class Re-mapping ---
# This dictionary maps the 80 COCO classes from YOLOv8 to our 4 waste categories

# Based on the object's typical material composition and common waste types
CLASS_MAP = {
    # Plastic items
    'bottle': 'Plastic',
    'cup': 'Plastic',
    'fork': 'Plastic',
    'knife': 'Plastic',
    'spoon': 'Plastic',
    'bowl': 'Plastic',
    'toothbrush': 'Plastic',
    'cell phone': 'Plastic',
    'remote': 'Plastic',
    'keyboard': 'Plastic',
    'mouse': 'Plastic',
    
    # Paper items
    'book': 'Paper',
    'newspaper': 'Paper',
    
    # Metal items
    'scissors': 'Metal',
    'refrigerator': 'Metal',
    'oven': 'Metal',
    'toaster': 'Metal',
    'sink': 'Metal',
    'fork': 'Metal',  # Can be metal or plastic
    'knife': 'Metal',
    'spoon': 'Metal',
    
    # Organic items
    'banana': 'Organic',
    'apple': 'Organic',
    'sandwich': 'Organic',
    'orange': 'Organic',
    'broccoli': 'Organic',
    'carrot': 'Organic',
    'hot dog': 'Organic',
    'pizza': 'Organic',
    'donut': 'Organic',
    'cake': 'Organic',
    
    # Default: Map unrecognized objects to "Other" or the best guess
}

def map_class_to_waste(label):
    """
    Maps a detected object label to one of the 4 waste categories
    Uses intelligent heuristics when exact mapping doesn't exist
    """
    # Direct mapping
    if label in CLASS_MAP:
        return CLASS_MAP[label]
    
    # Heuristic-based mapping for items not in the map
    # Food items -> Organic
    food_keywords = ['food', 'fruit', 'vegetable', 'meat', 'drink']
    if any(keyword in label.lower() for keyword in food_keywords):
        return 'Organic'
    
    # Electronic/plastic-looking items -> Plastic
    plastic_keywords = ['plastic', 'bottle', 'container', 'package', 'bag']
    if any(keyword in label.lower() for keyword in plastic_keywords):
        return 'Plastic'
    
    # Metal items
    metal_keywords = ['metal', 'can', 'tin', 'aluminum', 'steel']
    if any(keyword in label.lower() for keyword in metal_keywords):
        return 'Metal'
    
    # Paper items
    paper_keywords = ['paper', 'cardboard', 'box', 'newspaper', 'magazine']
    if any(keyword in label.lower() for keyword in paper_keywords):
        return 'Paper'
    
    # Default: Unknown items classified as "Other"
    return 'Other'

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Smart Waste Sorter API",
        "version": "1.0.0",
        "model": "YOLOv8n",
        "categories": ["Plastic", "Paper", "Metal", "Organic"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles image uploads, runs YOLOv8 inference, and returns
    structured JSON with detections and counts.
    
    Expected: multipart/form-data with 'image' field
    Returns: JSON with detections and category counts
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    try:
        # Read image bytes and open with PIL
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        print(f"\n{'='*60}")
        print(f"Processing image: {file.filename}")
        print(f"Image size: {img.size}")
        
        # Resize image to reduce memory usage
        max_size = 320  # Reduced from default 640 for free tier
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"Resized to: {img.size}")
        
        # Run inference on the image with confidence threshold
        results = model(img, conf=0.25, imgsz=320)  # 25% confidence, smaller image size
        
        detections = []
        counts = collections.defaultdict(int)
        
        # Process results
        for r in results:
            print(f"Detected {len(r.boxes)} objects")
            
            for box in r.boxes:
                # Extract box coordinates, confidence, and class
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf.item()
                cls_id = int(box.cls.item())
                label_from_model = model.names[cls_id]
                
                # Apply intelligent class mapping
                final_label = map_class_to_waste(label_from_model)
                
                print(f"  - Detected: {label_from_model} -> {final_label} ({conf:.2f})")
                
                # Append to detections list
                detections.append({
                    "box": [float(x1), float(y1), float(x2), float(y2)],
                    "label": final_label,
                    "originalLabel": label_from_model,
                    "confidence": float(conf)
                })
                
                counts[final_label] += 1
        
        print(f"Final counts: {dict(counts)}")
        print(f"{'='*60}\n")
        
        # Return the structured JSON response
        return jsonify({
            "success": True,
            "detections": detections,
            "counts": dict(counts),
            "total_objects": len(detections)
        })
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Returns the available waste categories"""
    return jsonify({
        "categories": ["Plastic", "Paper", "Metal", "Organic", "Other"],
        "description": {
            "Plastic": "Plastic bottles, containers, bags, and packaging",
            "Paper": "Paper, cardboard, newspapers, magazines",
            "Metal": "Aluminum cans, metal containers, foil",
            "Organic": "Food waste, fruits, vegetables, biodegradable items"
        }
    })

if __name__ == '__main__':
    import os
    
    print("\n" + "="*60)
    print("🚀 Starting Flask Backend Server")
    print("="*60)
    
    # Use PORT from environment (for deployment) or default to 5001 (for local dev)
    port = int(os.environ.get('PORT', 5001))
    
    print(f"Server will run on: http://0.0.0.0:{port}")
    print("API Endpoints:")
    print("  GET  / - Health check")
    print("  POST /predict - Image classification")
    print("  GET  /categories - Available waste categories")
    print("="*60 + "\n")
    
    # Run the app, accessible from any IP
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')

