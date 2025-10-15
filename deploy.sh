#!/bin/bash

echo "🚀 Telegram Trading Bot - Deployment Script"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "api_server.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Step 1: Build the frontend
echo "🏗️  Building frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

echo "🔨 Building production bundle..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful!"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

cd ..

# Step 2: Check git status
echo ""
echo "📋 Git status:"
git status --short

# Step 3: Provide deployment instructions
echo ""
echo "🎯 Next Steps for Deployment:"
echo ""
echo "1️⃣  CREATE GITHUB REPOSITORY:"
echo "   • Go to: https://github.com/new"
echo "   • Name: telegram-trading-bot"
echo "   • Description: Automated 24/7 Telegram Trading Signal Monitor"
echo "   • Public repository"
echo "   • Don't initialize (we have code already)"
echo ""

echo "2️⃣  PUSH TO GITHUB:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/telegram-trading-bot.git"
echo "   git push -u origin main"
echo ""

echo "3️⃣  DEPLOY FRONTEND TO VERCEL:"
echo "   • Go to: https://vercel.com/new"
echo "   • Import from GitHub: telegram-trading-bot"
echo "   • Framework: Vite"
echo "   • Root Directory: frontend"
echo "   • Build Command: npm run build"
echo "   • Output Directory: dist"
echo ""

echo "4️⃣  DEPLOY BACKEND TO RAILWAY:"
echo "   • Go to: https://railway.app/new"
echo "   • Deploy from GitHub: telegram-trading-bot"
echo "   • Root Directory: . (project root)"
echo "   • Start Command: python api_server.py"
echo ""

echo "5️⃣  UPDATE FRONTEND API URL:"
echo "   • In Vercel dashboard, add environment variable:"
echo "   • VITE_API_URL=https://your-backend-url.railway.app"
echo ""

echo "✨ Frontend build is ready in: frontend/dist/"
echo "🔗 All files are committed and ready to push to GitHub"
echo ""
echo "📚 For detailed instructions, see: DEPLOYMENT.md"
