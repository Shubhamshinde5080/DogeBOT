# Railway.app Deployment (Recommended - Free to start)
# ===================================================

## 🚂 **Why Railway.app?**
- ✅ **Free tier**: 500 hours/month (enough for testing)
- ✅ **Auto-deploy**: Connects to GitHub
- ✅ **Easy setup**: No server management
- ✅ **Scales**: Pay as you grow

## 📋 **Step-by-Step Deployment:**

### 1. **Prepare Your Repository**
```bash
# Add this file to your repo root
echo "web: python run.py" > Procfile

# Make sure these files exist:
# - Dockerfile ✅ (already created)
# - requirements.txt ✅ (already created)  
# - .env.sample ✅ (for reference)
```

### 2. **Deploy to Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your DogeBot repository
5. Railway auto-detects Dockerfile and deploys!

### 3. **Add Environment Variables**
In Railway dashboard, add:
```
API_KEY=your_binance_api_key
API_SECRET=your_binance_secret
BASE_URL=https://testnet.binance.vision
DAILY_TARGET=6.0
```

### 4. **Monitor Your Bot**
- Railway provides logs dashboard
- Bot runs 24/7 automatically
- Auto-restarts if it crashes

## 💰 **Cost Breakdown:**
- **Free**: 500 hours/month (20+ days)
- **Pro**: $5/month unlimited
- **Perfect for**: Crypto trading bots

## 🔗 **Alternative: Render.com (Also Free)**
Same process, also has free tier with GitHub integration.

## ⚡ **Quick Railway Deploy**
1. Push your code to GitHub
2. Connect Railway to your repo  
3. Add environment variables
4. Bot deploys automatically!

**Total setup time: 5 minutes!** 🚀
