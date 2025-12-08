# 🚀 Quick Start Guide

## ✅ Issue Fixed!

The `ajv/dist/compile/codegen` error has been resolved by reinstalling dependencies.
Both ports (5001 and 3000) have been cleared and are ready to use.

## 📝 How to Start the Application

You need **TWO separate terminal windows** - one for backend, one for frontend.

### Terminal 1: Start Backend

```bash
cd /Users/nova/Documents/swi-prolog/AI_LAB/waste_sorter
./start_backend.sh
```

**Wait for this message:**
```
✓ Model loaded successfully!
Server will run on: http://localhost:5001
* Running on http://127.0.0.1:5001
```

✅ **Keep this terminal open** - the backend is now running!

---

### Terminal 2: Start Frontend

Open a **NEW** terminal window and run:

```bash
cd /Users/nova/Documents/swi-prolog/AI_LAB/waste_sorter
./start_frontend.sh
```

**Wait for this message:**
```
Compiled successfully!
You can now view smart-sorter-ui in the browser.
Local: http://localhost:3000
```

✅ **Your browser will automatically open** to http://localhost:3000

---

## 🎯 Using the Application

1. **Choose an image** - Click "📁 Choose Image" and select a photo
2. **Classify** - Click "🔍 Classify Waste"  
3. **View results** - See bounding boxes and category counts!

### Good Test Images
- Kitchen photos with bottles, food, utensils
- Desk photos with books, pens, coffee cups
- Photos of fruits, vegetables, groceries
- Pictures of common objects

---

## 🐛 Troubleshooting

### Backend won't start (port 5001 in use)
```bash
# Kill the process and restart
lsof -ti:5001 | xargs kill -9
./start_backend.sh
```

### Frontend won't start (port 3000 in use)
```bash
# Kill the process and restart
lsof -ti:3000 | xargs kill -9
cd smart-sorter-ui && npm start
```

### "Cannot connect to backend" in browser
1. Make sure backend is running (check Terminal 1)
2. You should see "Running on http://127.0.0.1:5001"
3. Test: `curl http://localhost:5001/`

### Module errors in frontend
```bash
# Clean reinstall
cd smart-sorter-ui
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 📊 System Status Check

**Backend Test:**
```bash
curl http://localhost:5001/
```

Expected: JSON response with `"status": "online"`

**Frontend Test:**
Open http://localhost:3000 in your browser

Expected: See the Smart Waste Sorter UI

---

## 🎉 You're All Set!

Both servers should now be running:
- 🔧 Backend: http://localhost:5001
- 🎨 Frontend: http://localhost:3000

Upload an image and watch the AI classify your waste! 🗑️♻️


