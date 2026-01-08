"""
Gradio Interface for Smart Waste Sorter
Optimized for Hugging Face Spaces deployment
"""

import gradio as gr
import numpy as np
from PIL import Image
from ultralytics import YOLO
import collections

# Load model
print("Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')
print("✓ Model loaded!")

# Class mapping (same as Flask version)
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
    """Map detected object to waste category"""
    if label in CLASS_MAP:
        return CLASS_MAP[label]
    
    # Heuristic matching
    food_keywords = ['food', 'fruit', 'vegetable', 'meat']
    if any(keyword in label.lower() for keyword in food_keywords):
        return 'Organic'
    
    plastic_keywords = ['plastic', 'bottle', 'container']
    if any(keyword in label.lower() for keyword in plastic_keywords):
        return 'Plastic'
    
    metal_keywords = ['metal', 'can', 'tin', 'aluminum']
    if any(keyword in label.lower() for keyword in metal_keywords):
        return 'Metal'
    
    paper_keywords = ['paper', 'cardboard', 'box']
    if any(keyword in label.lower() for keyword in paper_keywords):
        return 'Paper'
    
    return 'Other'

def classify_waste(image):
    """
    Main classification function
    Args:
        image: PIL Image or numpy array
    Returns:
        annotated_image, results_text
    """
    if image is None:
        return None, "Please upload an image"
    
    # Convert to PIL if needed
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    
    print(f"Processing image of size: {image.size}")
    
    # Run inference
    results = model(image, conf=0.25)
    
    # Process results
    counts = collections.defaultdict(int)
    detections = []
    
    for r in results:
        print(f"Detected {len(r.boxes)} objects")
        for box in r.boxes:
            cls_id = int(box.cls.item())
            conf = box.conf.item()
            label_from_model = model.names[cls_id]
            final_label = map_class_to_waste(label_from_model)
            
            counts[final_label] += 1
            detections.append({
                'original': label_from_model,
                'category': final_label,
                'confidence': conf
            })
            print(f"  - {label_from_model} → {final_label} ({conf:.2%})")
    
    # Create results text
    results_text = "## 🗑️ Classification Results\n\n"
    
    if not counts:
        results_text += "❌ No waste items detected. Try another image with clearer objects!"
    else:
        results_text += f"**Total Items Detected:** {sum(counts.values())}\n\n"
        results_text += "### 📊 Category Breakdown:\n\n"
        
        # Sort by count (descending)
        for category, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            emoji = {
                'Plastic': '🔴',
                'Paper': '🟢',
                'Metal': '🔵',
                'Organic': '🟠',
                'Other': '⚪'
            }.get(category, '⚫')
            
            percentage = (count / sum(counts.values())) * 100
            results_text += f"{emoji} **{category}:** {count} item(s) ({percentage:.1f}%)\n\n"
        
        results_text += "\n---\n\n### 🔍 Detailed Detections:\n\n"
        for i, det in enumerate(detections, 1):
            results_text += f"{i}. **{det['original']}** → Category: `{det['category']}` (Confidence: {det['confidence']:.1%})\n"
        
        # Add recycling tips
        results_text += "\n---\n\n### ♻️ Recycling Tips:\n\n"
        for category in counts.keys():
            if category == 'Plastic':
                results_text += "🔴 **Plastic**: Rinse bottles and containers before recycling. Remove caps when possible.\n\n"
            elif category == 'Paper':
                results_text += "🟢 **Paper**: Keep paper dry and clean. Flatten cardboard boxes.\n\n"
            elif category == 'Metal':
                results_text += "🔵 **Metal**: Clean cans thoroughly. Watch for sharp edges.\n\n"
            elif category == 'Organic':
                results_text += "🟠 **Organic**: Compost at home or use municipal composting services.\n\n"
    
    # Return annotated image with bounding boxes
    annotated_image = results[0].plot()
    
    return Image.fromarray(annotated_image), results_text

# Create Gradio interface with modern theme
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🗑️ Smart Waste Sorter - AI-Powered Waste Classification
        
        Upload an image of waste items to automatically classify them into recycling categories using YOLOv8 object detection.
        
        ### Categories:
        - 🔴 **Plastic** - Bottles, containers, packaging, bags
        - 🟢 **Paper** - Cardboard, newspapers, magazines, boxes
        - 🔵 **Metal** - Aluminum cans, metal containers, foil
        - 🟠 **Organic** - Food waste, fruits, vegetables, biodegradable items
        - ⚪ **Other** - Items that don't fit standard categories
        """
    )
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(
                type="pil", 
                label="📤 Upload Waste Image",
                sources=["upload", "clipboard"]
            )
            classify_btn = gr.Button("🔍 Classify Waste", variant="primary", size="lg")
        
        with gr.Column():
            output_image = gr.Image(type="pil", label="🎯 Detected Objects")
            output_text = gr.Markdown(label="Classification Results")
    
    gr.Markdown(
        """
        ---
        ### ℹ️ How it works:
        1. Upload an image containing waste items
        2. Our AI model (YOLOv8) detects objects in the image
        3. Each object is classified into appropriate waste category
        4. View results with bounding boxes and recycling tips!
        
        **Tip:** For best results, use clear, well-lit photos with visible objects.
        """
    )
    
    # Button click event
    classify_btn.click(
        fn=classify_waste,
        inputs=input_image,
        outputs=[output_image, output_text]
    )
    
    # Examples (if you have test images)
    # gr.Examples(
    #     examples=[
    #         ["test/pet-plastic-bottles.jpg"],
    #         ["test/images.jpeg"],
    #     ],
    #     inputs=input_image
    # )

if __name__ == "__main__":
    demo.launch()

