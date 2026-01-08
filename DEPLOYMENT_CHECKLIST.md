# ✅ Deployment Checklist

## Pre-Deployment Checklist

### 1. Files to Commit
- [x] `render.yaml` - Updated with model download in build command
- [x] `Procfile` - Updated with model download in start command  
- [x] `app.py` - Added robust model loading
- [x] `requirements.txt` - Contains all dependencies including gunicorn
- [x] `load_model.py` - Model download script
- [ ] `smart-sorter-ui/.env.production` - Set correct API URL

### 2. Configuration Verification

#### Backend (`render.yaml` or `Procfile`)
```bash
# Check build command includes model download
grep "load_model.py" render.yaml
grep "load_model.py" Procfile

# Verify gunicorn is in requirements
grep "gunicorn" requirements.txt
```

#### Frontend (`.env.production`)
```bash
# Should point to your deployed backend
cat smart-sorter-ui/.env.production
# Expected: REACT_APP_API_URL=https://your-backend-url.onrender.com
```

### 3. Git Status
```bash
# Ensure all changes are committed
git status

# Should show: "nothing to commit, working tree clean"
```

## Deployment Steps

### Step 1: Commit and Push
```bash
git add render.yaml Procfile app.py README.md
git commit -m "Fix: Add model download to deployment pipeline (fixes exit 127)"
git push origin main
```

### Step 2: Monitor Deployment

#### For Render.com:
1. Go to Render Dashboard
2. Select your service
3. Click on "Logs" tab
4. Watch for these messages:
   - ✅ "Installing dependencies..."
   - ✅ "Loading YOLOv8 Model..."
   - ✅ "Model loaded successfully!"
   - ✅ "Starting Flask Backend Server"
   - ✅ "Live"

#### For Heroku:
```bash
heroku logs --tail --app your-app-name
```

### Step 3: Verify Deployment

#### Test 1: Health Check
```bash
curl https://your-app.onrender.com/
```

**Expected Response:**
```json
{
  "status": "online",
  "service": "Smart Waste Sorter API",
  "version": "1.0.0",
  "model": "YOLOv8n",
  "categories": ["Plastic", "Paper", "Metal", "Organic"]
}
```

#### Test 2: Predict Endpoint
```bash
curl -X POST \
  -F "image=@test/images.jpeg" \
  https://your-app.onrender.com/predict
```

**Expected:** JSON with detections array

#### Test 3: Categories Endpoint
```bash
curl https://your-app.onrender.com/categories
```

**Expected:** JSON with category descriptions

### Step 4: Deploy Frontend

```bash
cd smart-sorter-ui

# Update API URL
echo "REACT_APP_API_URL=https://your-backend.onrender.com" > .env.production

# Build
npm run build

# Deploy to Vercel/Netlify
# (Follow platform-specific instructions)
```

### Step 5: End-to-End Test

1. Open frontend URL in browser
2. Click "Choose Image"
3. Select a test image
4. Click "Classify Waste"
5. Verify results appear with bounding boxes

## Post-Deployment Checklist

- [ ] Backend health check returns 200 OK
- [ ] Predict endpoint works with test image
- [ ] Frontend can connect to backend
- [ ] Image upload works
- [ ] Classification results display correctly
- [ ] No console errors in browser
- [ ] Mobile responsiveness works
- [ ] Set up monitoring/alerts (optional)

## Troubleshooting

### If Deployment Still Fails:

#### Check Build Logs
Look for these specific errors:
- **"command not found"** → Missing package or typo
- **"timeout"** → Increase timeout value
- **"out of memory"** → Upgrade plan or use smaller model
- **"permission denied"** → File permission issues

#### Common Fixes:
```bash
# Verify Python version
python --version  # Should be 3.8+

# Test locally first
python load_model.py
python app.py

# Check requirements
pip install -r requirements.txt
```

#### Still Having Issues?
See `DEPLOYMENT_FIX.md` for detailed troubleshooting guide.

## Success Indicators

✅ Deployment complete when you see:
1. Build logs show "Model loaded successfully"
2. Health check endpoint returns 200
3. App shows "Live" status in dashboard
4. Can classify images via API

## Environment Variables (Optional)

Set these in your hosting platform if needed:

```bash
PORT=5001                    # Port number (auto-set on most platforms)
FLASK_ENV=production         # Production mode
PYTHON_VERSION=3.11.0        # Python version
```

## Performance Optimization (Optional)

```yaml
# For Render.com
workers: 2                   # Number of worker processes
timeout: 120                 # Request timeout in seconds
max_requests: 1000          # Restart workers after N requests
max_requests_jitter: 50     # Add randomness to avoid restart storms
```

## Monitoring Setup (Optional)

### Free Monitoring Tools:
- **UptimeRobot** - Uptime monitoring
- **Better Uptime** - Performance monitoring  
- **Render Built-in** - Metrics dashboard

### Set Up Alerts:
1. Create account on monitoring service
2. Add your deployment URL
3. Configure alerts (email/SMS)
4. Set check interval (5 minutes recommended)

## Backup and Rollback

### Create a Backup
```bash
git tag -a v1.0.0 -m "Working deployment"
git push origin v1.0.0
```

### Rollback if Needed
```bash
# List tags
git tag

# Rollback to previous version
git checkout v1.0.0

# Force push (be careful!)
git push origin main --force
```

Or use platform rollback features:
- **Render:** Dashboard → Rollback button
- **Heroku:** `heroku rollback`

## Resources

- 📖 [DEPLOYMENT_FIX.md](DEPLOYMENT_FIX.md) - Detailed troubleshooting
- 🚀 [QUICK_FIX.md](QUICK_FIX.md) - Quick reference
- 📘 [README.md](README.md) - Full documentation
- 🐳 [Dockerfile](Dockerfile) - Container deployment

---

**Last Updated:** January 8, 2026  
**Status:** Ready for deployment 🚀

