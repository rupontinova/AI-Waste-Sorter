"""
Flask Backend for Smart Waste Sorter - Hugging Face Deployment
Optimized for 16GB RAM on Hugging Face Spaces
"""

import io
import collections
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load model
print("="*60)
print("Loading YOLOv8 model for Hugging Face...")
model = YOLO('yolov8n.pt')
print("✓ Model loaded successfully!")
print("="*60)

# Class mapping
CLASS_MAP = {
    # Plastic items
    'bottle': 'Plastic',
    'cup': 'Plastic',
    'fork': 'Plastic',
    'knife': 'Plastic',
    'spoon': 'Plastic',
    'bowl': 'Plastic',
    'cell phone': 'Plastic',
    'remote': 'Plastic',
    'keyboard': 'Plastic',
    'mouse': 'Plastic',
    
    # Paper items
    'book': 'Paper',
    
    # Metal items
    'scissors': 'Metal',
    'refrigerator': 'Metal',
    'oven': 'Metal',
    'toaster': 'Metal',
    'sink': 'Metal',
    
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
}

def map_class_to_waste(label):
    if label in CLASS_MAP:
        return CLASS_MAP[label]
    
    food_keywords = ['food', 'fruit', 'vegetable', 'meat', 'drink']
    if any(keyword in label.lower() for keyword in food_keywords):
        return 'Organic'
    
    plastic_keywords = ['plastic', 'bottle', 'container', 'package', 'bag']
    if any(keyword in label.lower() for keyword in plastic_keywords):
        return 'Plastic'
    
    metal_keywords = ['metal', 'can', 'tin', 'aluminum', 'steel']
    if any(keyword in label.lower() for keyword in metal_keywords):
        return 'Metal'
    
    paper_keywords = ['paper', 'cardboard', 'box', 'newspaper', 'magazine']
    if any(keyword in label.lower() for keyword in paper_keywords):
        return 'Paper'
    
    return 'Other'

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Smart Waste Sorter API",
        "version": "1.0.0",
        "model": "YOLOv8n",
        "categories": ["Plastic", "Paper", "Metal", "Organic"],
        "deployed_on": "Hugging Face Spaces"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        print(f"Processing: {file.filename}, Size: {img.size}")
        
        # Run inference
        results = model(img, conf=0.25, imgsz=640)
        
        detections = []
        counts = collections.defaultdict(int)
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf.item()
                cls_id = int(box.cls.item())
                label_from_model = model.names[cls_id]
                final_label = map_class_to_waste(label_from_model)
                
                detections.append({
                    "box": [float(x1), float(y1), float(x2), float(y2)],
                    "label": final_label,
                    "originalLabel": label_from_model,
                    "confidence": float(conf)
                })
                
                counts[final_label] += 1
        
        print(f"Detected: {dict(counts)}")
        
        return jsonify({
            "success": True,
            "detections": detections,
            "counts": dict(counts),
            "total_objects": len(detections)
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/categories', methods=['GET'])
def get_categories():
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
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False)

