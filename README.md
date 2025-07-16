# DogeBot - Automated DOGE Trading Bot

A production-ready automated trading bot for DOGE/FDUSD using grid trading strategies with technical indicators.

## 🚀 Features

- **Grid Trading Strategy**: Automated buy/sell orders at predefined price levels
- **Technical Indicators**: ATR, EMA, Bollinger Band percentage for entry signals
- **Real-time Data**: Live WebSocket connection to Binance for 15-minute OHLC data
- **Risk Management**: Position sizing based on ATR and configurable risk parameters
- **Monitoring**: Prometheus metrics and health checks for production monitoring
- **Security**: Environment-based configuration with no hardcoded credentials
- **Testing**: Comprehensive test suite with pytest
- **Logging**: Structured logging with configurable levels

## 📋 Prerequisites

- Docker and Docker Compose
- Binance account with API access
- Redis (included in Docker setup)

## 🔧 Installation & Setup

### 1. Clone and Configure

```bash
git clone https://github.com/yourusername/DogeBot.git
cd DogeBot

# Copy environment template
cp .env.sample .env

# Edit environment variables
nano .env
```

### 2. Environment Variables

Configure your `.env` file with the following required variables:

```bash
# Binance API Configuration
EXCHANGE=testnet  # or 'live' for production
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# For testnet
BASE_URL=https://testnet.binance.vision/api

# For live trading (uncomment when ready)
# BASE_URL=https://api.binance.com/api

# Trading Parameters
SYMBOL=DOGEFDUSD
RISK_PERCENT=1.0
MAX_POSITION_SIZE=1000
GRID_LEVELS=5

# WebSocket Configuration
WS_STREAM_URL=wss://stream.binance.com:9443/ws
KLINE_INTERVAL=15m

# Monitoring
REDIS_URL=redis://redis:6379/0
LOG_LEVEL=INFO
```

### 3. Deploy with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f dogebot

# Health check
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

## 📊 Monitoring

### Health Endpoints

- **Health Check**: `GET /health` - Service status
- **Ready Check**: `GET /ready` - WebSocket connectivity status
- **Metrics**: `GET /metrics` - Prometheus metrics

### Key Metrics

- `bot_realised_pnl` - Realized profit/loss
- `bot_open_ladders` - Number of active grid levels
- `websocket_messages_total` - WebSocket message count
- `strategy_signals_total` - Trading signal count

### Log Files

```bash
# Application logs
docker-compose logs dogebot

# WebSocket logs
tail -f /tmp/dogebot_websocket.log

# Strategy logs  
tail -f /tmp/dogebot_strategy.log
```

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=bot --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Slow tests only

# Test specific components
pytest tests/test_indicators.py
pytest tests/test_strategy.py
```

## 🔒 Security Best Practices

### Environment Protection

- ✅ `.env` files excluded from git
- ✅ No hardcoded API keys in code
- ✅ Secrets managed via environment variables
- ✅ Docker secrets for production deployment

### API Security

- Use testnet for development and testing
- Enable IP restrictions on Binance API keys
- Use separate API keys for testnet and production
- Regularly rotate API keys

### Production Deployment

```bash
# Use Docker secrets for production
echo "your_api_key" | docker secret create binance_api_key -
echo "your_secret_key" | docker secret create binance_secret_key -

# Update docker-compose.yml to use secrets
# See docker-compose.prod.yml for example
```

## 📈 Strategy Configuration

### Grid Trading Parameters

The bot uses a grid trading strategy with the following parameters:

- **Entry Condition**: Bollinger Band % ≤ 0.15 (low volatility)
- **Trend Filter**: Price > 0.97 × EMA50 (uptrend confirmation)
- **Position Sizing**: Based on ATR14 × risk percentage
- **Grid Levels**: Configurable number of buy/sell orders
- **Risk Management**: Maximum position size limits

### Technical Indicators

- **ATR (Average True Range)**: Volatility-based position sizing
- **EMA (Exponential Moving Average)**: Trend direction filter
- **Bollinger Band %**: Mean reversion entry signals

## 🐛 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   ```bash
   # Check network connectivity
   curl -I https://stream.binance.com:9443/ws
   
   # Verify symbol name (DOGEFDUSD is correct)
   grep SYMBOL .env
   ```

2. **API Authentication Errors**
   ```bash
   # Test API keys
   docker-compose exec dogebot python -c "
   from binance.client import Client
   import os
   client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'))
   print(client.get_account_status())
   "
   ```

3. **No Trading Signals**
   ```bash
   # Check indicator calculations
   docker-compose logs dogebot | grep "📊 Candles collected"
   
   # Verify strategy conditions
   docker-compose logs dogebot | grep "Strategy"
   ```

### Debug Mode

```bash
# Enable debug logging
echo "LOG_LEVEL=DEBUG" >> .env
docker-compose restart dogebot

# Watch real-time logs
docker-compose logs -f dogebot
```

## 🚦 Production Deployment

### Pre-deployment Checklist

- [ ] Tested on Binance testnet
- [ ] Environment variables configured
- [ ] API key permissions verified
- [ ] Risk parameters reviewed
- [ ] Monitoring alerts configured
- [ ] Backup strategies in place

### Production Docker Compose

```yaml
version: '3.8'
services:
  dogebot:
    build: .
    env_file: .env.prod
    secrets:
      - binance_api_key
      - binance_secret_key
    environment:
      - BINANCE_API_KEY_FILE=/run/secrets/binance_api_key
      - BINANCE_SECRET_KEY_FILE=/run/secrets/binance_secret_key
    restart: unless-stopped
    
secrets:
  binance_api_key:
    external: true
  binance_secret_key:
    external: true
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This software is for educational purposes only. Trading cryptocurrencies involves substantial risk of loss and is not suitable for all investors. The authors are not responsible for any financial losses incurred through the use of this software.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

- Create an issue for bug reports
- Join our Discord for community support
- Check the troubleshooting section above
