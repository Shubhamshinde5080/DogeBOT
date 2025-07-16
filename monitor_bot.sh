#!/bin/bash
# DogeBot Monitoring Dashboard
echo "🤖     for asset in ['FDUSD', 'DOGE'];ogeBot Live Monitoring Dashboard"
echo "====================================="
echo "⏰ $(date)"
echo ""

# Container Status
echo "🐳 Container Status:"
docker ps | grep dogebot | head -1
echo ""

# Resource Usage
echo "📊 Resource Usage:"
docker stats dogebot-container --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
echo ""

# Recent Logs (last 10 lines)
echo "📝 Recent Activity (last 10 lines):"
docker logs dogebot-container --tail 10
echo ""

# Network Connectivity Check
echo "🌐 Network Status:"
# Check if bot is actually receiving data (WebSocket working)
if docker logs dogebot-container --tail 20 | grep -q "WebSocket handshake successful\|Subscribing to DOGEFDUSD"; then
    echo "✅ Bot WebSocket: Connected and Active"
else
    echo "❌ Bot WebSocket: No activity detected"
fi

# Test API connectivity from inside container
docker exec dogebot-container python -c "
import requests
try:
    response = requests.get('https://testnet.binance.vision/api/v3/ping', timeout=5)
    print('✅ Binance Testnet API: Connected' if response.status_code == 200 else '❌ Binance Testnet API: Error')
except:
    print('❌ Binance Testnet API: Connection failed')
" 2>/dev/null
echo ""

# Account Balance Check
echo "💰 Current Account Status:"
python -c "
from bot.utils.account_monitor import AccountMonitor
try:
    monitor = AccountMonitor()
    price = monitor.get_current_price('DOGEFDUSD')
    balances = monitor.get_account_balance()
    print(f'  📊 DOGEFDUSD Price: \${price:.6f}')
    
    for asset in ['FDUSD', 'DOGE']:
        if asset in balances and balances[asset]['total'] > 0:
            bal = balances[asset]
            print(f'  💰 {asset}: {bal[\"total\"]:.2f} total ({bal[\"free\"]:.2f} free)')
except Exception as e:
    print(f'  ❌ Account check failed: {str(e)[:50]}')
" 2>/dev/null
echo ""

# Last few log lines with timestamp
echo "🕐 Latest Bot Activity:"
docker logs dogebot-container --tail 3 --timestamps | sed 's/^/  /'
echo ""

echo "🔄 Refreshing every 30 seconds... (Ctrl+C to stop)"
