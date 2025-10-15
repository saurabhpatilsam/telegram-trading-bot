#!/bin/bash

echo "🚀 Deploying Frontend to Vercel..."
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "api_server.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Navigate to frontend
cd frontend

echo "🔧 Checking Vercel CLI..."
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo ""
echo "🎯 Deployment Options:"
echo ""
echo "Option 1: Vercel Dashboard (Recommended)"
echo "  1. Go to: https://vercel.com/new"
echo "  2. Import: telegram-trading-bot repository"
echo "  3. Root Directory: frontend"
echo "  4. Framework: Vite"
echo "  5. Environment Variable:"
echo "     VITE_API_URL=https://telegram-bot-api-production-0d7e.up.railway.app"
echo ""
echo "Option 2: Vercel CLI"
echo "  Run: vercel login"
echo "  Then: vercel --prod"
echo ""

read -p "Do you want to try Vercel CLI deployment? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔐 Please login to Vercel first..."
    vercel login
    
    echo ""
    echo "🚀 Deploying to production..."
    vercel --prod
else
    echo "📋 Please use the Vercel Dashboard option:"
    echo "   https://vercel.com/new"
    echo ""
    echo "✅ Backend is ready at:"
    echo "   https://telegram-bot-api-production-0d7e.up.railway.app"
fi

echo ""
echo "🎉 After deployment, your complete system will be live!"
echo "   Frontend: Your Vercel URL"
echo "   Backend:  https://telegram-bot-api-production-0d7e.up.railway.app"
echo "   Database: Supabase (configured)"
