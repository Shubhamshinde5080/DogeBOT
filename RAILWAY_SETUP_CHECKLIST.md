# 🚀 Railway Environment Setup Checklist

## ✅ Required Environment Variables 

Go to Railway Dashboard → Your DogeBot Project → Settings → Shared Variables

### 🔑 Required Variables:
```
BINANCE_API_KEY = your_testnet_api_key
BINANCE_API_SECRET = your_testnet_secret
BASE_URL = https://testnet.binance.vision
STREAM_URL = wss://stream.binance.vision/ws
DAILY_TARGET = 6.0
FDUSD_CAP = 1100
```

### 📱 Optional Notifications:
```
DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/...
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_CHAT_ID = your_chat_id
```

## 🔍 Health Check List

- [ ] ✅ Shared Variables populated
- [ ] ✅ Logs streaming in Railway Web tab  
- [ ] ✅ No "BASE_URL env = None" errors
- [ ] ✅ "REST API initialized with BASE_URL: https://testnet.binance.vision"
- [ ] ✅ WebSocket connected successfully
- [ ] ✅ Market data streaming (15m klines)
- [ ] ✅ Strategy active, placing orders
- [ ] ✅ PnL tracking working
- [ ] ✅ Webhook notifications firing (if configured)

## 🎯 Success Indicators

**Logs should show:**
```
✅ REST API initialized with BASE_URL: https://testnet.binance.vision
🔧 Environment variables mapped for Railway.app deployment
   API_KEY: ✅
   API_SECRET: ✅
   BASE_URL: https://testnet.binance.vision

📊 Strategy: WAIT (collecting data...)
💰 SELL FILL: +$0.0123 profit | Total PnL: $1.2345 | Target: $6.0
```

## 🚨 Red Flags to Fix

❌ `BASE_URL env = None`  
❌ `Invalid URL '12/api/v3/order'`  
❌ `BB = nan` warnings (normal for first 20 candles)  
❌ No trade executions after 30+ minutes  

## 📱 Quick Discord Setup

1. Create Discord server
2. Add webhook: Server Settings → Integrations → Webhooks → New Webhook
3. Copy webhook URL to Railway variable `DISCORD_WEBHOOK_URL`
4. Bot will send trade notifications automatically

## 🎉 You're Done When...

- Bot runs 24/7 without crashes
- Makes profitable DOGEFDUSD trades  
- Stops at $6 daily profit
- Sends notifications to your phone
- Railway shows stable ~75MB RAM usage
