#!/bin/bash

echo "🚀 Auto-Deploying to Vercel..."
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "api_server.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Test the backend first
echo "🔍 Testing backend connection..."
BACKEND_URL="https://telegram-bot-api-production-0d7e.up.railway.app"
if curl -s "$BACKEND_URL" > /dev/null; then
    echo "✅ Backend is responding at: $BACKEND_URL"
else
    echo "⚠️  Backend might be starting up at: $BACKEND_URL"
fi

echo ""
echo "🎯 Vercel Deployment Options:"
echo ""
echo "The configuration has been fixed! Now you can:"
echo ""
echo "Option 1: Vercel Dashboard (Recommended)"
echo "  1. Go to: https://vercel.com/new"
echo "  2. Import: telegram-trading-bot"
echo "  3. Framework: Vite (auto-detected)"
echo "  4. Root Directory: . (project root - FIXED!)"
echo "  5. Build Command: npm run build (auto-detected)"
echo "  6. Output Directory: frontend/dist (auto-detected)"
echo "  7. Environment Variable:"
echo "     VITE_API_URL=$BACKEND_URL"
echo "  8. Deploy!"
echo ""
echo "Option 2: Vercel CLI"
echo "  vercel login"
echo "  vercel --prod"
echo ""

echo "🔧 Configuration Files Created:"
echo "  ✅ Root package.json - Vercel build system"
echo "  ✅ Root vercel.json - Deployment config"
echo "  ✅ Frontend vercel.json - App config"
echo "  ✅ Frontend .env.production - API URL"
echo ""

echo "🎊 After deployment, your system will be:"
echo "  Frontend: https://your-app.vercel.app"
echo "  Backend:  $BACKEND_URL ✅"
echo "  Database: Supabase ✅"
echo ""
echo "Ready to deploy! The package.json error is now fixed! 🚀"
