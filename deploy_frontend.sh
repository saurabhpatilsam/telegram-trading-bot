#!/bin/bash

echo "🚀 Deploying Frontend to Vercel..."
echo "=================================="
echo ""

# Navigate to frontend directory
cd frontend

# Check if logged in to Vercel
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami > /dev/null 2>&1; then
    echo "❌ Not logged in to Vercel"
    echo "Please run: vercel login"
    echo "Then run this script again"
    exit 1
fi

echo "✅ Logged in to Vercel as: $(vercel whoami)"
echo ""

# Set environment variables
echo "⚙️  Setting environment variables..."
echo "VITE_API_URL=https://telegram-bot-api-production-0d7e.up.railway.app" > .env.production

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod --yes

echo ""
echo "✅ Frontend deployment initiated!"
echo ""
echo "🌐 Your app will be available at the URL shown above"
echo "📊 Dashboard: https://vercel.com/dashboard"
echo ""
echo "🎉 Complete system is now deployed:"
echo "   Frontend: Vercel"
echo "   Backend:  Railway (https://telegram-bot-api-production-0d7e.up.railway.app)"
echo "   Database: Supabase"
echo ""
echo "Ready to monitor Telegram channels 24/7! 🚀"
