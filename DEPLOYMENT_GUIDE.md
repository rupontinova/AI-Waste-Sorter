# 🚀 Deployment Guide - Smart Waste Sorter

This guide will help you deploy your waste classification system **completely free** using Render (backend) and Vercel (frontend).

---

## 📋 Prerequisites

1. GitHub account
2. Git installed locally
3. Your project pushed to GitHub

---

## 🎯 Deployment Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  Frontend (Vercel)  │ ← React App (Port 443/HTTPS)
└─────────┬───────────┘
          │
          │ API Calls
          ▼
┌───────────────────────┐
│  Backend (Render)     │ ← Flask API + YOLOv8
│  Python + ML Model    │
└───────────────────────┘
```

---

## 🔧 Step 1: Prepare Your Project for Deployment

### 1.1 Push to GitHub

```bash
cd /Users/nova/Documents/swi-prolog/AI_LAB/waste_sorter

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/waste-sorter.git
git branch -M main
git push -u origin main
```

**⚠️ Important:** Make sure `yolov8n.pt` is included in your repository (it's only 6.2 MB).

---

## 🐍 Step 2: Deploy Backend on Render

### 2.1 Sign Up for Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### 2.2 Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your `waste-sorter` repository

### 2.3 Configure the Service
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `waste-sorter-backend` (or any name) |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` |

### 2.4 Add Environment Variables (Optional)
- Click **"Advanced"**
- Add: `PYTHON_VERSION` = `3.11.0`

### 2.5 Deploy!
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. You'll get a URL like: `https://waste-sorter-backend.onrender.com`

### 2.6 Test Your Backend
```bash
# Test health endpoint
curl https://waste-sorter-backend.onrender.com/

# Should return:
# {"status": "online", "service": "Smart Waste Sorter API", ...}
```

---

## ⚛️ Step 3: Deploy Frontend on Vercel

### 3.1 Update Frontend API URL

First, update your React app to use the Render backend URL:

```bash
cd smart-sorter-ui
```

Create a `.env.production` file:

```bash
echo "REACT_APP_API_URL=https://waste-sorter-backend.onrender.com" > .env.production
```

Update `src/App.js` to use the environment variable:

Find this line (around line 15):
```javascript
const API_URL = 'http://localhost:5001';
```

Replace with:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
```

Commit the changes:
```bash
git add .
git commit -m "Configure production API URL"
git push
```

### 3.2 Sign Up for Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### 3.3 Deploy Frontend
1. Click **"Add New..."** → **"Project"**
2. Import your `waste-sorter` repository
3. Configure:

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Create React App` |
| **Root Directory** | `smart-sorter-ui` |
| **Build Command** | `npm run build` |
| **Output Directory** | `build` |

4. Add Environment Variable:
   - Key: `REACT_APP_API_URL`
   - Value: `https://waste-sorter-backend.onrender.com` (your Render URL)

5. Click **"Deploy"**

6. You'll get a URL like: `https://waste-sorter.vercel.app`

---

## ✅ Step 4: Test Your Deployed App

1. Open your Vercel URL in a browser
2. Upload a test image from the `test/` folder
3. Verify the classification works!

---

## 🎉 Alternative Deployment Options

### Option 2: Hugging Face Spaces (Best for ML Apps)

**Backend + Frontend in One Place!**

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create a new Space
3. Choose **"Gradio"** or **"Streamlit"**
4. Upload your code

**Pros:**
- ✅ Free GPU available
- ✅ Perfect for ML models
- ✅ Simple single deployment
- ✅ No cold starts

**Cons:**
- ⚠️ Requires converting to Gradio/Streamlit interface

### Option 3: Railway.app (Backend + Frontend)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Deploy from GitHub repo
4. $5 free credit/month
5. Auto-detects Python and Node.js

### Option 4: Fly.io (Backend)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
flyctl launch
```

---

## 🔒 Security & Production Best Practices

### 1. Environment Variables
Never commit sensitive data. Use `.env` files:

```bash
# Backend .env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Frontend .env
REACT_APP_API_URL=https://your-backend-url.com
```

### 2. CORS Configuration
Update `app.py` for production:

```python
from flask_cors import CORS

# Restrict CORS to your frontend domain
CORS(app, origins=["https://waste-sorter.vercel.app"])
```

### 3. Rate Limiting
Add Flask-Limiter to prevent abuse:

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 4. Error Monitoring
Add Sentry for error tracking:

```bash
pip install sentry-sdk[flask]
```

---

## 📊 Free Tier Limitations

| Platform | Limits | Notes |
|----------|--------|-------|
| **Render** | 750 hrs/month, 512MB RAM | Spins down after 15 min inactivity |
| **Vercel** | 100GB bandwidth/month | More than enough for small apps |
| **Hugging Face** | Unlimited (with fair use) | Best for ML models |
| **Railway** | $5 credit/month (~500 hours) | No auto-sleep |

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Model not loading
```bash
# Solution: Ensure yolov8n.pt is in repository
ls -lh yolov8n.pt
# Should be ~6.2 MB
```

**Problem:** Out of memory on Render
```bash
# Solution: Use YOLOv8n (nano) instead of larger models
# Already using the smallest model ✓
```

**Problem:** Cold start too slow
```bash
# Solution: Upgrade to Render paid plan ($7/month)
# or use Railway/Fly.io instead
```

### Frontend Issues

**Problem:** API calls failing (CORS)
```javascript
// Check browser console for errors
// Update CORS in app.py to allow your Vercel domain
```

**Problem:** Images not displaying
```javascript
// Ensure API_URL is correct in .env.production
console.log(process.env.REACT_APP_API_URL);
```

### DNS & Custom Domains

Both Vercel and Render support custom domains:

1. **Vercel:** Settings → Domains → Add
2. **Render:** Settings → Custom Domain

---

## 💰 Cost Comparison

| Solution | Cost | Best For |
|----------|------|----------|
| **Render + Vercel** | $0/month | Most users, reliable |
| **Hugging Face** | $0/month | ML demos, portfolios |
| **Railway** | $5/month (free credit) | No cold starts needed |
| **Fly.io** | ~$0-5/month | Advanced users |

---

## 🚀 Quick Deploy Commands

### Deploy Backend (Render)
```bash
# Already configured! Just:
# 1. Push to GitHub
# 2. Connect Render to your repo
# 3. Click "Deploy"
```

### Deploy Frontend (Vercel)
```bash
# Install Vercel CLI (optional)
npm i -g vercel

# Deploy
cd smart-sorter-ui
vercel

# Follow prompts, done!
```

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Hugging Face Spaces:** https://huggingface.co/docs/hub/spaces

---

## ✅ Post-Deployment Checklist

- [ ] Backend health check returns 200 OK
- [ ] Frontend loads without errors
- [ ] Image upload and prediction works
- [ ] Bounding boxes display correctly
- [ ] Category counts update properly
- [ ] Error messages show for invalid inputs
- [ ] Mobile responsive design works
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Custom domain configured (optional)

---

## 🎯 Final URLs

After deployment, update this section:

- **Frontend:** https://waste-sorter.vercel.app
- **Backend API:** https://waste-sorter-backend.onrender.com
- **GitHub Repo:** https://github.com/YOUR_USERNAME/waste-sorter

---

## 🎉 Congratulations!

Your AI waste classification system is now live and accessible to anyone with the URL!

**Share your project:**
- Add to your portfolio
- Share on LinkedIn/Twitter
- Include in your resume
- Demo to potential employers

---

*Last Updated: January 2026*

