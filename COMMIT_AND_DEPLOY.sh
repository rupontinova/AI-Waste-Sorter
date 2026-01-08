#!/bin/bash

# Smart Waste Sorter - Deployment Fix Commit Script
# This script commits the fixes and prepares for deployment

echo "=========================================="
echo "🚀 Smart Waste Sorter Deployment Fix"
echo "=========================================="
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository"
    echo "   Please run this script from the project root"
    exit 1
fi

echo "📋 Files that will be committed:"
echo ""
git status --short
echo ""

# Show the key changes
echo "🔧 Key Changes Made:"
echo "   ✅ render.yaml - Added model download to build"
echo "   ✅ Procfile - Added model download to start"
echo "   ✅ app.py - Enhanced model loading logic"
echo "   ✅ README.md - Added troubleshooting section"
echo "   ✅ Documentation - Created fix guides"
echo ""

# Confirm with user
read -p "Do you want to commit these changes? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📦 Staging files..."
    git add render.yaml Procfile app.py README.md
    git add DEPLOYMENT_FIX.md QUICK_FIX.md DEPLOYMENT_CHECKLIST.md FIX_SUMMARY.md
    
    echo "✅ Files staged"
    echo ""
    
    echo "💬 Creating commit..."
    git commit -m "Fix: Resolve deployment exit 127 - Add model download pipeline

- Update render.yaml to download model during build
- Update Procfile to ensure model availability
- Enhance app.py with robust model loading
- Add comprehensive deployment documentation
- Increase timeout to 120s for model loading
- Configure workers and port binding

This fixes the 'Exited with status 127' error by ensuring
the YOLOv8 model is downloaded before the app starts."
    
    echo "✅ Commit created"
    echo ""
    
    echo "🎯 Next Steps:"
    echo ""
    echo "1. Push to deploy:"
    echo "   git push origin main"
    echo ""
    echo "2. Monitor deployment in Render dashboard"
    echo "   Look for: 'Model loaded successfully!'"
    echo ""
    echo "3. Test the deployed API:"
    echo "   curl https://your-app.onrender.com/"
    echo ""
    echo "4. Update frontend .env.production with API URL"
    echo ""
    
    read -p "Push to origin now? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Pushing to origin..."
        git push origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "=========================================="
            echo "✅ SUCCESS!"
            echo "=========================================="
            echo ""
            echo "Your fixes have been pushed!"
            echo ""
            echo "📊 Monitor deployment:"
            echo "   Render: https://dashboard.render.com"
            echo "   Heroku: heroku logs --tail"
            echo ""
            echo "⏱️  Expected deployment time: 3-5 minutes"
            echo ""
            echo "📖 Need help? See:"
            echo "   - DEPLOYMENT_FIX.md (detailed guide)"
            echo "   - QUICK_FIX.md (quick reference)"
            echo "   - DEPLOYMENT_CHECKLIST.md (step-by-step)"
            echo ""
            echo "Good luck! 🎉"
            echo "=========================================="
        else
            echo ""
            echo "❌ Push failed"
            echo "   Check your git credentials and try:"
            echo "   git push origin main"
        fi
    else
        echo ""
        echo "⏸️  Push skipped"
        echo "   When ready, run: git push origin main"
    fi
else
    echo ""
    echo "⏸️  Commit cancelled"
    echo "   No changes were committed"
fi

echo ""

