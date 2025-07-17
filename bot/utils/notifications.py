#!/usr/bin/env python3
"""
Discord/Telegram webhook notifications for DogeBot
"""
import os
import requests
import asyncio
from datetime import datetime

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_notification(message: str, level: str = "INFO"):
    """Send notification to Discord and/or Telegram"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"🤖 **DogeBot** `{timestamp}` {message}"
    
    # Discord webhook
    if DISCORD_WEBHOOK_URL:
        try:
            emoji = {"INFO": "📊", "SUCCESS": "✅", "ERROR": "❌", "PROFIT": "💰"}.get(level, "📊")
            requests.post(DISCORD_WEBHOOK_URL, json={
                "content": f"{emoji} {formatted_message}"
            }, timeout=5)
        except Exception as e:
            print(f"Discord notification failed: {e}")
    
    # Telegram
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": formatted_message,
                "parse_mode": "Markdown"
            }, timeout=5)
        except Exception as e:
            print(f"Telegram notification failed: {e}")

# Convenience functions
def notify_trade(action: str, price: float, qty: int, pnl: float = None):
    if pnl:
        send_notification(f"{action} {qty} DOGE @ ${price:.6f} | PnL: ${pnl:.4f}", "PROFIT")
    else:
        send_notification(f"{action} {qty} DOGE @ ${price:.6f}", "SUCCESS")

def notify_target_hit(pnl: float, target: float):
    send_notification(f"🎯 DAILY TARGET HIT! PnL: ${pnl:.4f} >= ${target:.4f}", "SUCCESS")

def notify_error(error: str):
    send_notification(f"Error: {error}", "ERROR")
