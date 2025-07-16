# DogeBot Railway.app Deployment Guide

## 🚀 Deploy DogeBot to Railway.app for 24/7 Operation

### Step 1: Prepare Your Repository
```bash
# Ensure all files are committed
git add .
git commit -m "DogeBot ready for deployment"
git push origin main
```

### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your DogeBot repository
4. Railway will automatically detect the Dockerfile and deploy

### Step 3: Configure Environment Variables
In Railway dashboard, go to Variables tab and add:

```
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_secret_here  
DOGEFDUSD_DAILY_TARGET_USD=6
DOGEFDUSD_MAX_FUND_USD=1100
```

### Step 4: Monitor Deployment
- Check logs for: "WebSocket handshake successful"
- Verify: "Subscribing to DOGEFDUSD 15m klines"
- Monitor: Candle collection and condition checking

### Step 5: Access Your Bot
- Your bot will be available at: `https://your-app-name.railway.app`
- Dashboard: `https://your-app-name.railway.app/dashboard`
- Health check: `https://your-app-name.railway.app/health`

## 🔥 Expected Behavior

1. **Startup** (0-2 minutes):
   - WebSocket connects to Binance
   - Starts collecting 15-minute candles

2. **Data Collection** (15-150 minutes):
   - Collects 10 candles for technical analysis
   - Calculates Bollinger Bands and EMA

3. **Trading Ready** (After 10 candles):
   - Monitors for entry conditions: BB ≤ 0.30 AND EMA > 0.95
   - Starts automated buy/sell when conditions align

## 📊 Monitoring Commands

```bash
# Check deployment status
railway status

# View live logs  
railway logs

# Connect to shell (if needed)
railway shell
```

## 🎯 Success Indicators

✅ **"WebSocket handshake successful"** - Connected to market data
✅ **"Closed 15-min candle"** - Receiving live data  
✅ **"Waiting for BB ≤ 0.30"** - Strategy engine active
✅ **"Cycle START"** - Trading conditions met, bot trading

## 🚨 Troubleshooting

### If bot doesn't start:
- Check environment variables are set correctly
- Verify Binance API keys have testnet permissions
- Check Railway logs for specific errors

### If no trading activity:
- Bot needs 10 candles (2.5 hours) before trading
- Entry conditions are strict: BB ≤ 0.30 AND EMA > 0.95
- Market volatility must align with conditions

## 💰 Expected Performance

- **Daily Target**: $6 USD profit
- **Max Investment**: $1,100 USD  
- **Strategy**: Grid trading with Bollinger Band + EMA filters
- **Trading Hours**: 24/7 automated operation

Your DogeBot is now ready for continuous 24/7 operation! 🚀
