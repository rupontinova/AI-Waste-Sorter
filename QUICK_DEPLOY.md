# ⚡ Quick Deploy Cheat Sheet

Choose your deployment method and follow the steps!

---

## 🚀 Method 1: Render + Vercel (Full Stack)

**Best for:** Production apps with custom UI  
**Time:** 15 minutes  
**Cost:** $0/month

### Backend (Render)

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to render.com → New Web Service
# 3. Connect GitHub repo
# 4. Settings:
#    - Build: pip install -r requirements.txt
#    - Start: gunicorn app:app
#    - Environment: Python 3

# 5. Copy your backend URL (e.g., https://your-app.onrender.com)
```

### Frontend (Vercel)

```bash
# 1. Update API URL in smart-sorter-ui/.env.production
echo "REACT_APP_API_URL=https://your-render-backend-url.onrender.com" > smart-sorter-ui/.env.production

# 2. Push changes
git add .
git commit -m "Update production API URL"
git push

# 3. Go to vercel.com → New Project
# 4. Import GitHub repo
# 5. Settings:
#    - Root Directory: smart-sorter-ui
#    - Framework: Create React App
#    - Build Command: npm run build
#    - Output Directory: build
#    - Env Variable: REACT_APP_API_URL = your backend URL

# 6. Deploy!
```

**Done! Your app is live at your Vercel URL** 🎉

---

## 🤗 Method 2: Hugging Face Spaces (Gradio)

**Best for:** ML demos, portfolios, quick sharing  
**Time:** 5 minutes  
**Cost:** $0/month (with free GPU!)

```bash
# 1. Create Space at huggingface.co/spaces
# 2. Choose Gradio SDK

# 3. Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/waste-sorter
cd waste-sorter

# 4. Copy required files
cp ../waste_sorter/app_gradio.py app.py
cp ../waste_sorter/requirements_gradio.txt requirements.txt
cp ../waste_sorter/yolov8n.pt .

# 5. Push to Hugging Face
git add .
git commit -m "Deploy waste sorter"
git push

# 6. Done! App is live at:
# https://huggingface.co/spaces/YOUR_USERNAME/waste-sorter
```

---

## 🐳 Method 3: Docker (Any Platform)

**Best for:** Self-hosting, cloud providers  
**Time:** 10 minutes  
**Cost:** Varies by platform

```bash
# 1. Build Docker image
docker build -t waste-sorter .

# 2. Run locally (test)
docker run -p 5001:5001 waste-sorter

# 3. Deploy to:
#    - Google Cloud Run
#    - AWS ECS
#    - Azure Container Apps
#    - DigitalOcean App Platform
#    - Railway (auto-detects Dockerfile)
```

---

## 🆓 Free Hosting Comparison

| Platform | Backend | Frontend | GPU | Cold Start | Limit |
|----------|---------|----------|-----|------------|-------|
| **Render** | ✅ Free | ❌ | ❌ | Yes (15 min) | 750 hrs/month |
| **Vercel** | ❌ | ✅ Free | ❌ | No | 100GB bandwidth |
| **HF Spaces** | ✅ Free | ✅ Free | ✅ Optional | No | Fair use |
| **Railway** | ✅ $5 credit | ✅ $5 credit | ❌ | No | ~500 hrs/month |
| **Fly.io** | ✅ Free | ✅ Free | ❌ | No | 3 VMs |

---

## 📋 Pre-Deployment Checklist

- [ ] Project pushed to GitHub
- [ ] `yolov8n.pt` model file included (6.2 MB)
- [ ] `requirements.txt` up to date
- [ ] Frontend API URL updated for production
- [ ] Test locally first
- [ ] Read full `DEPLOYMENT_GUIDE.md` if issues

---

## 🐛 Quick Troubleshooting

### Backend won't start
```bash
# Check logs for:
# "Model not found" → Ensure yolov8n.pt is in repo
# "Out of memory" → You're using the smallest model already ✓
# "Port in use" → Use $PORT environment variable
```

### Frontend can't connect to backend
```javascript
// Check API URL in browser console:
console.log(process.env.REACT_APP_API_URL)

// Update .env.production if wrong
```

### CORS errors
```python
# In app.py, update CORS to allow your frontend domain:
CORS(app, origins=["https://your-frontend.vercel.app"])
```

---

## 💡 Pro Tips

1. **Render Free Tier:** Spins down after 15 min → First request takes ~30s
2. **Vercel:** Unlimited deploys, automatic HTTPS, custom domains free
3. **HF Spaces:** Enable GPU for $0.60/hr (T4) for faster inference
4. **Keep model small:** YOLOv8n is perfect for free tiers
5. **Test locally first:** `./start_backend.sh` & `./start_frontend.sh`

---

## 🎯 Recommended Combinations

| Use Case | Best Setup |
|----------|-----------|
| Portfolio/Demo | Hugging Face Spaces |
| School Project | Render + Vercel |
| Production MVP | Railway (paid) or Render + Vercel |
| Quick Test | Hugging Face Spaces |
| Learning | Any of the above! |

---

## 🔗 Quick Links

- Full guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- HF Spaces guide: [DEPLOY_HUGGINGFACE.md](DEPLOY_HUGGINGFACE.md)
- Render: https://render.com
- Vercel: https://vercel.com
- Hugging Face: https://huggingface.co/spaces

---

## ✅ After Deployment

1. Test with images from `test/` folder
2. Share your live URL!
3. Add to portfolio/resume
4. Consider:
   - Custom domain (free on Vercel/Render)
   - Analytics (Google Analytics)
   - Error monitoring (Sentry)

---

**Questions?** Check `DEPLOYMENT_GUIDE.md` for detailed instructions.

**Good luck!** 🚀

