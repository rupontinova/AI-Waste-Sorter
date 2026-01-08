# 🚀 Deploy to Hugging Face Spaces (FREE & EASY!)

## Why Hugging Face?
- ✅ **16GB RAM** (vs 512MB on Render)
- ✅ **100% FREE** for public apps
- ✅ **Made for AI models** like YOLOv8
- ✅ **No credit card required**

---

## 📦 Required Files (Already Created!)

You already have:
- ✅ `app_gradio.py` - Gradio interface
- ✅ `requirements_gradio.txt` - Dependencies
- ✅ `load_model.py` - Model loader

Just need 2 small config files:

---

## Step 1: Create `app.py` for Hugging Face

```python
# This file will launch the Gradio app
from app_gradio import *

if __name__ == "__main__":
    demo.launch()
```

---

## Step 2: Create `README.md` for Hugging Face Space

```markdown
---
title: Smart Waste Sorter
emoji: 🗑️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app_gradio.py
pinned: false
---

# Smart Waste Sorter

AI-powered waste classification using YOLOv8.
```

---

## Step 3: Deploy!

### Method A: Via Hugging Face Website (Easiest!)

1. Go to: https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Settings:
   - **Space name:** `smart-waste-sorter`
   - **License:** Apache 2.0
   - **SDK:** Gradio
   - **Hardware:** CPU Basic (FREE)
4. Click **"Create Space"**
5. Upload files:
   - `app_gradio.py`
   - `requirements_gradio.txt`
   - `load_model.py`
   - `README.md` (from step 2)
6. Wait 2-3 minutes
7. **Done!** 🎉

### Method B: Via Git (Advanced)

```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/smart-waste-sorter
cd smart-waste-sorter

# Copy files
cp ../waste_sorter/app_gradio.py .
cp ../waste_sorter/requirements_gradio.txt requirements.txt
cp ../waste_sorter/load_model.py .

# Create README.md (see step 2)

# Push
git add .
git commit -m "Initial commit"
git push
```

---

## 🎉 Success!

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/smart-waste-sorter
```

**No out of memory errors!** 🚀

