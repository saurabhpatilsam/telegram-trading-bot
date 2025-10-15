# 🚀 Deployment Guide

## Frontend Deployment to Vercel

### Option 1: Vercel CLI (Recommended)

1. **Install Vercel CLI** (already done):
```bash
npm install -g vercel
```

2. **Navigate to frontend directory**:
```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo/frontend
```

3. **Deploy to Vercel**:
```bash
vercel --prod
```

4. **Follow the prompts**:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N** 
   - What's your project's name? **telegram-trading-bot-frontend**
   - In which directory is your code located? **.**
   - Want to modify settings? **N**

### Option 2: Vercel Dashboard

1. **Go to** https://vercel.com/dashboard
2. **Click "New Project"**
3. **Import from Git** (after creating GitHub repo)
4. **Configure**:
   - Framework Preset: **Vite**
   - Root Directory: **frontend**
   - Build Command: **npm run build**
   - Output Directory: **dist**
   - Install Command: **npm install**

### Environment Variables for Production

Add these in Vercel dashboard:

```
VITE_API_URL=https://your-backend-api-url.com
```

## Backend Deployment Options

### Option 1: Railway (Recommended for Python)

1. **Go to** https://railway.app
2. **Connect GitHub repository**
3. **Deploy backend**:
   - Root Directory: **.**
   - Start Command: **python api_server.py**
   - Port: **8000**

### Option 2: Render

1. **Go to** https://render.com
2. **New Web Service**
3. **Connect repository**
4. **Configure**:
   - Environment: **Python 3**
   - Build Command: **pip install -r backend_requirements.txt**
   - Start Command: **python api_server.py**

### Option 3: Heroku

1. **Create Procfile**:
```
web: python api_server.py
```

2. **Deploy**:
```bash
heroku create telegram-trading-bot-api
git push heroku main
```

## GitHub Repository Setup

### Manual Creation

1. **Go to** https://github.com/new
2. **Repository name**: `telegram-trading-bot`
3. **Description**: `Automated 24/7 Telegram Trading Signal Monitor with React Dashboard and AI Analysis`
4. **Public repository**
5. **Create repository**

### Push Code

```bash
cd /Users/stagnator/Downloads/Telegram_supabase_Algo
git remote add origin https://github.com/YOUR_USERNAME/telegram-trading-bot.git
git branch -M main
git push -u origin main
```

## Production Configuration

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend-api.railway.app
```

### Backend Environment Variables
```env
# Telegram
TELEGRAM_API_ID=20831057
TELEGRAM_API_HASH=your_hash
TELEGRAM_PHONE=+447405502859

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Supabase
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
SUPABASE_TABLE=trading_signals

# Production
PORT=8000
HOST=0.0.0.0
```

## Post-Deployment Steps

1. **Update frontend API URL** to point to deployed backend
2. **Test all functionality**:
   - Add channel
   - Start monitoring
   - View signals
3. **Set up monitoring** (optional)
4. **Configure custom domain** (optional)

## Deployment URLs

After deployment, you'll have:

- **Frontend**: `https://telegram-trading-bot-frontend.vercel.app`
- **Backend**: `https://telegram-trading-bot-api.railway.app`
- **GitHub**: `https://github.com/YOUR_USERNAME/telegram-trading-bot`

## Security Notes

- ✅ Never commit `.env` files
- ✅ Use environment variables in production
- ✅ Enable CORS for your frontend domain only
- ✅ Consider adding authentication for production use

## Monitoring

### Vercel
- Automatic deployments on git push
- Function logs and analytics
- Performance monitoring

### Railway/Render
- Application logs
- Resource usage monitoring
- Automatic scaling

## Troubleshooting

### Build Errors
- Check Node.js version compatibility
- Verify all dependencies are installed
- Review build logs

### Runtime Errors
- Check environment variables
- Verify API endpoints
- Review application logs

### CORS Issues
- Update backend CORS settings
- Add production domain to allowed origins

## Cost Estimation

### Free Tiers
- **Vercel**: 100GB bandwidth, unlimited projects
- **Railway**: $5/month after free tier
- **Render**: 750 hours/month free

### Paid Plans
- **Vercel Pro**: $20/month
- **Railway**: Usage-based pricing
- **Render**: $7/month for web services

## Next Steps

1. **Deploy frontend to Vercel**
2. **Deploy backend to Railway**
3. **Update API URL in frontend**
4. **Test production deployment**
5. **Set up monitoring and alerts**
