# 🤗 Deploy to Hugging Face Spaces

This guide shows you how to deploy your Waste Sorter app to Hugging Face Spaces - **perfect for ML projects with FREE GPU access!**

---

## 🌟 Why Hugging Face Spaces?

- ✅ **100% Free** (with optional paid upgrades)
- ✅ **GPU Available** for faster inference
- ✅ **No Cold Starts** - always running
- ✅ **Perfect for ML Models**
- ✅ **Built-in Sharing & Embedding**
- ✅ **Single Deployment** (frontend + backend together)

---

## 🚀 Quick Deploy (5 Minutes)

### Step 1: Create Account
1. Go to [huggingface.co](https://huggingface.co)
2. Sign up (free)

### Step 2: Create a Space
1. Click your profile → **"New Space"**
2. Fill in:
   - **Space name:** `waste-sorter`
   - **SDK:** Choose **Gradio**
   - **Hardware:** Start with **CPU basic** (free)
   - **Visibility:** Public or Private

### Step 3: Convert to Gradio

We need to create a Gradio interface instead of Flask. Here's the code:

Create `app_gradio.py`:

```python
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
    
    # Paper items
    'book': 'Paper',
    
    # Metal items
    'scissors': 'Metal',
    'refrigerator': 'Metal',
    
    # Organic items
    'banana': 'Organic',
    'apple': 'Organic',
    'sandwich': 'Organic',
    'orange': 'Organic',
    'broccoli': 'Organic',
    'carrot': 'Organic',
    'pizza': 'Organic',
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
    
    # Run inference
    results = model(image, conf=0.25)
    
    # Process results
    counts = collections.defaultdict(int)
    detections = []
    
    for r in results:
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
    
    # Create results text
    results_text = "## 🗑️ Classification Results\n\n"
    
    if not counts:
        results_text += "No waste items detected. Try another image!"
    else:
        results_text += f"**Total Items:** {sum(counts.values())}\n\n"
        results_text += "### Category Breakdown:\n"
        
        for category, count in sorted(counts.items()):
            emoji = {
                'Plastic': '🔴',
                'Paper': '🟢',
                'Metal': '🔵',
                'Organic': '🟠',
                'Other': '⚪'
            }.get(category, '⚫')
            
            results_text += f"- {emoji} **{category}:** {count} item(s)\n"
        
        results_text += "\n### Detected Objects:\n"
        for det in detections:
            results_text += f"- {det['original']} → {det['category']} ({det['confidence']:.2%})\n"
    
    # Return annotated image
    annotated_image = results[0].plot()
    
    return Image.fromarray(annotated_image), results_text

# Create Gradio interface
demo = gr.Interface(
    fn=classify_waste,
    inputs=gr.Image(type="pil", label="Upload Waste Image"),
    outputs=[
        gr.Image(type="pil", label="Detected Objects"),
        gr.Markdown(label="Classification Results")
    ],
    title="🗑️ Smart Waste Sorter",
    description="""
    Upload an image of waste items to automatically classify them into categories:
    - 🔴 **Plastic** - Bottles, containers, packaging
    - 🟢 **Paper** - Cardboard, newspapers, magazines
    - 🔵 **Metal** - Cans, foil, metal containers
    - 🟠 **Organic** - Food waste, fruits, vegetables
    
    Powered by YOLOv8 object detection.
    """,
    examples=[
        ["test/pet-plastic-bottles.jpg"],
        ["test/images.jpeg"],
    ] if False else None,  # Add your test images
    theme=gr.themes.Soft(),
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
```

### Step 4: Create `requirements.txt` for Spaces

```txt
ultralytics>=8.0.0
gradio>=4.0.0
torch>=2.0.0
torchvision>=0.15.0
opencv-python-headless>=4.8.0
Pillow>=10.0.0
numpy>=1.24.0
```

### Step 5: Upload Files to Space

You can upload files through:

**Option A: Web Interface**
1. Go to your Space → **Files**
2. Upload:
   - `app_gradio.py` → rename to `app.py`
   - `requirements.txt`
   - `yolov8n.pt`
3. Space will auto-build!

**Option B: Git (Recommended)**

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/waste-sorter
cd waste-sorter

# Copy files
cp /path/to/your/app_gradio.py app.py
cp /path/to/your/requirements.txt .
cp /path/to/your/yolov8n.pt .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Step 6: Access Your App!

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/waste-sorter
```

---

## ⚙️ Configuration Options

### Enable GPU (Optional)

1. Go to Space → **Settings** → **Hardware**
2. Upgrade to:
   - **T4 Small** (Free tier available!)
   - **T4 Medium** ($0.60/hr)
   - **A10G Small** ($1.05/hr)

For this project, **CPU is fine** - GPU is overkill for YOLOv8n.

### Private Space

1. Settings → **Visibility**
2. Change to **Private**

### Custom Domain

1. Settings → **Advanced**
2. Add custom domain (free!)

---

## 📊 Space Structure

Your Hugging Face Space should look like:

```
waste-sorter/
├── app.py              # Gradio interface (renamed from app_gradio.py)
├── requirements.txt    # Python dependencies
├── yolov8n.pt         # YOLOv8 model (6.2 MB)
├── README.md          # Space description (optional)
└── examples/          # Example images (optional)
```

---

## 🎨 Gradio vs Flask Comparison

| Feature | Flask (Original) | Gradio (Spaces) |
|---------|------------------|-----------------|
| **Deployment** | Separate frontend + backend | Single file |
| **UI** | Custom React | Auto-generated |
| **Sharing** | Need hosting | Built-in |
| **GPU** | Manual setup | One-click |
| **Cost** | Varies | Free tier |

---

## 🔧 Troubleshooting

### Model Not Loading

```python
# If yolov8n.pt isn't found, download it automatically:
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Will auto-download if missing
```

### Out of Memory

1. Use **CPU** instead of GPU (for YOLOv8n)
2. Or upgrade to larger hardware

### Slow Inference

1. Enable GPU (T4 Small is free!)
2. Or reduce image size:

```python
# In classify_waste function:
image = image.resize((640, 640))
```

---

## 🚀 Advanced Features

### Add Webcam Support

```python
inputs=gr.Image(type="pil", label="Upload or Capture", sources=["upload", "webcam"])
```

### Add Examples

```python
examples=[
    "examples/plastic_bottle.jpg",
    "examples/apple.jpg",
    "examples/newspaper.jpg"
]
```

### Add Statistics Tracking

```python
# Use Hugging Face Datasets to log results
from datasets import Dataset

def log_result(category, count):
    # Your logging code here
    pass
```

---

## 📱 Embedding Your Space

You can embed your Space on any website:

```html
<gradio-app src="https://huggingface.co/spaces/YOUR_USERNAME/waste-sorter"></gradio-app>
<script type="module" src="https://gradio.s3-us-west-2.amazonaws.com/4.0.0/gradio.js"></script>
```

---

## 🏆 Benefits Summary

✅ **One-click deployment**
✅ **Free GPU available**
✅ **No cold starts**
✅ **Built-in sharing**
✅ **Version control**
✅ **Community visibility**
✅ **Mobile-friendly UI**

---

## 🆚 When to Use What?

| Use Case | Best Platform |
|----------|---------------|
| **Portfolio/Demo** | Hugging Face Spaces |
| **Custom UI** | Vercel + Render |
| **Production App** | Google Cloud / AWS |
| **Quick Test** | Hugging Face Spaces |
| **Learning** | Hugging Face Spaces |

---

## 📞 Resources

- **Gradio Docs:** https://www.gradio.app/docs/
- **Spaces Docs:** https://huggingface.co/docs/hub/spaces
- **Examples:** https://huggingface.co/spaces

---

*Deployment time: ~5 minutes*
*Cost: $0/month*
*Difficulty: ⭐⭐☆☆☆*

**Perfect for portfolios, demos, and learning!** 🎉

