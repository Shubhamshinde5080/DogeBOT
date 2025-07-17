# DogeBot Account & Price Monitoring

## 🎯 Features Added

Your DogeBot now includes comprehensive account monitoring and enhanced logging capabilities to help you track both your trading performance and market conditions.

## 📊 Current Price Monitoring

### Check DOGEFDUSD and DOGEUSDT Prices
```bash
# Check all prices and stats
docker-compose exec bot python /app/check_account.py --all

# Check just current prices  
docker-compose exec bot python /app/check_account.py --price

# Check specific symbol
docker-compose exec bot python /app/check_account.py --price --symbol BTCUSDT
```

### Sample Output:
```
📊 Current Prices:
  DOGEUSDT: $0.201110
  DOGEFDUSD: $0.201510

📈 24h Statistics (DOGEUSDT):
  Price: $0.201110
  Change: 📈 +0.008720 (+4.53%)
  High: $0.988710
  Low: $0.175810
  Volume: 163,462,975 DOGE
```

## 💰 Account Balance Monitoring

### Check Account Balances
```bash
# Check account balances (requires valid API credentials)
docker-compose exec bot python /app/check_account.py --balance

# Full summary with balances and prices
docker-compose exec bot python /app/check_account.py --all
```

## 🎯 Daily Target System

### Enhanced Trading Controls
- **Daily Profit Target**: Set `DAILY_TARGET=6.0` in your `.env` file
- **Automatic Reset**: Resets every day at midnight UTC
- **Trading Pause**: Bot stops trading when daily target is reached
- **Continuous Logging**: See real-time status updates

### Log Messages You'll See:
```
🌄 New day reset – realised PnL cleared
🎯 Daily target reached (6.00) - stopping trading
⏰ Waiting for next candle... 
🔔 ▶️ Cycle START – entry=0.201110, ATR=0.003456
📋 Order placed: BUY 100.0 DOGEUSDT @ 0.201000
✅ Order filled: BUY 100.0 DOGEUSDT @ 0.201000
```

## 🔧 Usage Examples

### 1. Quick Price Check
```bash
docker-compose exec bot python /app/check_account.py --price
```

### 2. Monitor Account Status
```bash
docker-compose exec bot python /app/check_account.py --all
```

### 3. Check Specific Crypto
```bash
docker-compose exec bot python /app/check_account.py --price --symbol ETHUSDT
```

### 4. View Live Bot Logs
```bash
docker-compose logs --tail=50 bot
```

## 📈 Enhanced Logging Features

### What's Now Logged:
1. **Daily Reset Events** - When profit targets reset at midnight UTC
2. **Target Achievement** - When daily profit goals are reached
3. **Waiting States** - Continuous status while waiting for next signals
4. **Cycle Starts** - When new trading cycles begin with entry prices
5. **Order Events** - Detailed order placement, fills, and errors
6. **System Status** - Connection states, subscriptions, and health checks

### Log Monitoring:
```bash
# Live log stream
docker-compose logs -f bot

# Recent activity
docker-compose logs --tail=20 bot

# Search for specific events
docker-compose logs bot | grep "🎯\|🌄\|🔔"
```

## 🛠️ API Requirements

### For Price Monitoring:
- ✅ **No API keys required** - Uses public Binance endpoints
- ✅ **Real-time prices** for DOGEUSDT and DOGEFDUSD
- ✅ **24h statistics** including volume, high, low, and change

### For Account Balance:
- ⚠️ **API credentials required** - Set `API_KEY` and `API_SECRET` in `.env`
- 💼 **Account balances** for all assets
- 📊 **Portfolio summary** with total values

## 🚀 Integration with Main Bot

The monitoring utilities integrate seamlessly with your existing DogeBot:

1. **Price data** uses the same Binance connection as your trading bot
2. **Account monitoring** can run alongside live trading
3. **Daily targets** work with your existing grid strategy
4. **Enhanced logging** provides better visibility into bot decisions

## 💡 Pro Tips

1. **Monitor regularly**: Run price checks periodically to stay informed
2. **Set daily targets**: Use the `DAILY_TARGET` feature to manage risk
3. **Watch the logs**: Enhanced logging shows exactly what your bot is doing
4. **Track both symbols**: DOGEFDUSD often has different spreads than DOGEUSDT

Your DogeBot is now equipped with comprehensive monitoring capabilities! 🚀
