#!/bin/bash

echo "🎯 DogeBot Enhanced Logging Demo"
echo "================================"
echo ""
echo "📋 Features Added:"
echo "✅ Daily $6 target enforcement"
echo "✅ Continuous 'waiting' logs every candle"
echo "✅ 'BUY/SELL' transaction logging"
echo "✅ Cycle start notifications"
echo "✅ Faster testing (10 candles vs 30)"
echo ""

echo "🔍 What you'll see in the logs:"
echo "🌄 New day reset – realised PnL cleared"
echo "⏳ Waiting – price=0.123456, ATR=0.001234"
echo "🔔 ▶️ Cycle START – entry=0.123456, ATR=0.001234"
echo "🔨 Placing BUY – price=0.123400, qty=300"
echo "✅ BUY filled – price=0.123401, qty=300"
echo "🎯 Daily target $6.00 reached – waiting for tomorrow"
echo ""

echo "📊 Current Status:"
docker-compose ps

echo ""
echo "🎬 Live Logs (Ctrl+C to stop):"
echo "==============================="

# Follow logs with enhanced output
docker logs -f dogebot_bot_1 | while read line; do
    case "$line" in
        *"🌄 New day reset"*)
            echo "$(date '+%H:%M:%S') 🌅 $line"
            ;;
        *"⏳ Waiting"*)
            echo "$(date '+%H:%M:%S') ⌛ $line"
            ;;
        *"🔔 ▶️ Cycle START"*)
            echo "$(date '+%H:%M:%S') 🚀 $line"
            ;;
        *"🔨 Placing"*)
            echo "$(date '+%H:%M:%S') 💰 $line"
            ;;
        *"✅"*"filled"*)
            echo "$(date '+%H:%M:%S') ✅ $line"
            ;;
        *"🎯 Daily target"*)
            echo "$(date '+%H:%M:%S') 🏆 $line"
            ;;
        *"💹 Closed 15-min candle"*)
            echo "$(date '+%H:%M:%S') 📊 $line"
            ;;
        *)
            echo "$(date '+%H:%M:%S') 📋 $line"
            ;;
    esac
done
