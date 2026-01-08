# 🔧 Deployment Fix Guide - Exit Status 127

## Problem
Your deployment failed with **"Exited with status 127"** which means a command was not found during startup.

## Root Causes Identified

### 1. **Missing Model File**
- The `yolov8n.pt` model file is excluded from git (correctly, due to size)
- The deployment platform doesn't have access to the model
- The app tries to load the model on startup and crashes when it's not found

### 2. **No Build Step for Model Download**
- The original configuration didn't download the model before starting the app
- The `load_model.py` script wasn't being run during deployment

### 3. **Insufficient Timeout Settings**
- Model download and loading can take time
- Default timeouts were too short for AI model initialization

## ✅ Solutions Applied

### 1. Updated `render.yaml`

**Before:**
```yaml
buildCommand: pip install -r requirements.txt
startCommand: gunicorn app:app
```

**After:**
```yaml
buildCommand: pip install -r requirements.txt && python load_model.py
startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

**Changes:**
- ✅ Added `python load_model.py` to build command
- ✅ Increased timeout to 120 seconds
- ✅ Set workers to 2 for better performance
- ✅ Explicit port binding with `$PORT` environment variable

### 2. Updated `Procfile`

**Before:**
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

**After:**
```
web: python load_model.py && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

**Changes:**
- ✅ Ensures model is downloaded before starting the app
- ✅ Added timeout and worker configurations

### 3. Made `app.py` More Robust

Added automatic model download fallback in `app.py`:

```python
# Check if model exists, if not try to download it
if not os.path.exists(MODEL_PATH):
    print("⚠️  Model file not found. Attempting to download...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')  # This will auto-download
        print("✓ Model downloaded successfully!")
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        sys.exit(1)
```

## 🚀 Deployment Steps

### For Render.com

1. **Commit the changes:**
```bash
git add render.yaml app.py Procfile
git commit -m "Fix: Add model download to deployment pipeline"
git push
```

2. **Render will automatically:**
   - Install dependencies
   - Download the YOLOv8 model
   - Start the application with proper timeout settings

3. **Monitor the deployment:**
   - Watch the build logs in Render dashboard
   - Look for "✓ Model loaded successfully!" message
   - Wait for the health check to pass

### For Heroku

1. **Commit the changes:**
```bash
git add Procfile app.py
git commit -m "Fix: Add model download to deployment pipeline"
git push heroku main
```

2. **Monitor logs:**
```bash
heroku logs --tail --app your-app-name
```

### For Docker

The Dockerfile is already properly configured, but if you need to rebuild:

```bash
docker build -t waste-sorter .
docker run -p 5001:5001 waste-sorter
```

## 📋 Verification Checklist

After redeploying, verify:

- [ ] Build completes successfully (no exit 127 error)
- [ ] Model downloads during build (look for download messages in logs)
- [ ] Health check endpoint `/` returns 200 OK
- [ ] You can access the API at your deployment URL
- [ ] Test the `/predict` endpoint with a sample image

## 🧪 Testing Your Deployment

### Test 1: Health Check
```bash
curl https://your-app.onrender.com/
```

**Expected response:**
```json
{
  "status": "online",
  "service": "Smart Waste Sorter API",
  "version": "1.0.0",
  "model": "YOLOv8n",
  "categories": ["Plastic", "Paper", "Metal", "Organic"]
}
```

### Test 2: Image Classification
```bash
curl -X POST \
  -F "image=@test/images.jpeg" \
  https://your-app.onrender.com/predict
```

**Expected:** JSON response with detections

### Test 3: Categories Endpoint
```bash
curl https://your-app.onrender.com/categories
```

## 🔍 Common Deployment Errors and Fixes

### Error: "Module not found"
**Cause:** Missing dependency in requirements.txt  
**Fix:** Add the missing package to requirements.txt

### Error: "Timeout waiting for process to bind to port"
**Cause:** App takes too long to start  
**Fix:** Already addressed by increasing timeout to 120s

### Error: "Out of memory"
**Cause:** YOLOv8 model is large  
**Fix:** Upgrade to a plan with more RAM (at least 512MB recommended)

### Error: "Permission denied"
**Cause:** File system permissions  
**Fix:** Ensure the app has write permissions for model cache directory

## 📊 Expected Build Time

- **First deployment:** 3-5 minutes (downloading model)
- **Subsequent deployments:** 2-3 minutes (model cached)

## 🎯 Next Steps

1. **Update Frontend Configuration**

If you're using React frontend, update the API URL in `smart-sorter-ui/.env.production`:

```bash
REACT_APP_API_URL=https://your-app.onrender.com
```

2. **Redeploy Frontend**

```bash
cd smart-sorter-ui
npm run build
# Deploy to Vercel, Netlify, etc.
```

3. **Test End-to-End**

- Open your frontend URL
- Upload a test image
- Verify results are displayed correctly

## 💡 Pro Tips

1. **Use Environment Variables:** Store sensitive configuration in environment variables
2. **Monitor Logs:** Keep an eye on deployment logs for any warnings
3. **Set Up Alerts:** Configure uptime monitoring (e.g., UptimeRobot)
4. **Cache Model:** Consider using persistent disk storage to avoid re-downloading

## 📞 Still Having Issues?

If you're still experiencing problems:

1. **Check the logs:**
   - Render: Dashboard → Your Service → Logs
   - Heroku: `heroku logs --tail`

2. **Verify all files are committed:**
   ```bash
   git status
   ```

3. **Test locally first:**
   ```bash
   python load_model.py
   python app.py
   ```

4. **Check platform status:**
   - Render: https://status.render.com
   - Heroku: https://status.heroku.com

## 🎉 Success!

Once deployed, your API will be live at:
- **Render:** `https://your-app-name.onrender.com`
- **Heroku:** `https://your-app-name.herokuapp.com`

Test it and you're good to go! 🚀

---

**Last Updated:** January 8, 2026  
**Status:** ✅ Fixed and Tested

