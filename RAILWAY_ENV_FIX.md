# 🚀 Railway Environment Variables Setup

## 🐛 Problem Identified
Railway is setting `BASE_URL=12` (probably the port number) which breaks API calls.

## ✅ Required Environment Variables in Railway

Go to your Railway app dashboard → Variables tab and set these **EXACTLY**:

### 🔑 Binance API Credentials
```
BINANCE_API_KEY=your_binance_testnet_api_key_here
BINANCE_API_SECRET=your_binance_testnet_secret_here
```

### 🌐 Base URL Override
```
BINANCE_BASE_URL=https://testnet.binance.vision
```

### 💰 Trading Configuration
```
DAILY_TARGET=6.0
FDUSD_CAP=1100
```

## 🔍 Debug Steps

1. **Check Current Logs**: Look at Railway deployment logs for debug output showing environment variables
2. **Set Variables**: Add the above variables in Railway dashboard
3. **Redeploy**: Railway should automatically redeploy after setting variables
4. **Verify Fix**: Look for successful API calls in logs

## 🎯 Expected Log Output After Fix

You should see:
```
🔧 Environment variables mapped for Railway.app deployment
   API_KEY: ✅
   API_SECRET: ✅
   BASE_URL: https://testnet.binance.vision
   DAILY_TARGET: 6.0
   FDUSD_CAP: 1100

🔍 DEBUG: BASE_URL env = 'https://testnet.binance.vision'
```

## 🚨 Important Notes

- **BINANCE_BASE_URL** (not BASE_URL) - this prevents Railway from overriding it
- Use your **testnet** credentials (not production)
- Railway auto-redeploys when you add variables
- Check logs within 1-2 minutes after setting variables

## 🔧 Alternative Fix

If Railway keeps overriding BASE_URL, you can also set:
```
FORCE_TESTNET=true
```

The bot will detect this and force testnet URL regardless of other settings.
