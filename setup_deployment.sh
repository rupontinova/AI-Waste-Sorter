#!/bin/bash

# Setup script for deployment
# This script prepares your project for deployment

echo "================================================"
echo "   Smart Waste Sorter - Deployment Setup"
echo "================================================"
echo ""

# Create .env.production for frontend
echo "Creating environment files..."
echo ""

# .env.production (you'll need to update this with your actual backend URL)
cat > smart-sorter-ui/.env.production << 'EOF'
# Production API URL - Update this after deploying backend to Render
REACT_APP_API_URL=https://waste-sorter-backend.onrender.com
EOF

echo "✓ Created smart-sorter-ui/.env.production"

# .env.development for frontend
cat > smart-sorter-ui/.env.development << 'EOF'
# Development API URL - Local Flask server
REACT_APP_API_URL=http://localhost:5001
EOF

echo "✓ Created smart-sorter-ui/.env.development"

echo ""
echo "================================================"
echo "   Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. IMPORTANT: Update the API URL in smart-sorter-ui/.env.production"
echo "   after you deploy your backend to Render"
echo ""
echo "2. Choose your deployment method:"
echo "   - Easiest: Read DEPLOY_NOW.md (Hugging Face Spaces)"
echo "   - Full-stack: Read DEPLOYMENT_GUIDE.md (Render + Vercel)"
echo ""
echo "3. Test locally first:"
echo "   Terminal 1: ./start_backend.sh"
echo "   Terminal 2: ./start_frontend.sh"
echo ""
echo "Good luck! 🚀"
echo ""

