import asyncio
from fastapi import FastAPI, Response
from prometheus_client import Gauge, generate_latest

# Debug environment variables first
print("🚀 DogeBot Starting - Debug Environment Variables:")
import os
print("🔍 ALL ENVIRONMENT VARIABLES:")
for key, value in sorted(os.environ.items()):
    if any(term in key.upper() for term in ['API', 'BASE', 'URL', 'BINANCE', 'DAILY', 'FDUSD', 'PORT']):
        display_value = value[:10] + '...' if len(value) > 10 else value
        print(f"   {key} = {display_value}")

print("\n🎯 EXPECTED VARIABLES:")
expected = ['BINANCE_API_KEY', 'BINANCE_API_SECRET', 'BINANCE_BASE_URL', 'DAILY_TARGET', 'FDUSD_CAP']
for var in expected:
    value = os.getenv(var)
    status = '✅' if value else '❌'
    print(f"   {status} {var} = {value[:10] + '...' if value and len(value) > 10 else value}")

try:
    from bot.services.websocket import strategy, start_websocket
except Exception as e:
    print(f"❌ WebSocket import failed: {e}")
    import traceback
    traceback.print_exc()

app = FastAPI()

# Start WebSocket immediately when module is imported
try:
    import threading
    def start_ws():
        asyncio.run(start_websocket())
    
    ws_thread = threading.Thread(target=start_ws, daemon=True)
    ws_thread.start()
except Exception as e:
    print(f"❌ Failed to start WebSocket thread: {e}")
    import traceback
    traceback.print_exc()

# Initialize metrics with safe registration
try:
    pnl_g = Gauge("bot_realised_pnl", "Realised PnL")
    ladder_g = Gauge("bot_open_ladders", "# open ladders")
except ValueError:
    # Metrics already registered, get existing ones
    from prometheus_client import REGISTRY
    for collector in list(REGISTRY._collector_to_names.keys()):
        if hasattr(collector, '_name'):
            if collector._name == "bot_realised_pnl":
                pnl_g = collector
            elif collector._name == "bot_open_ladders":
                ladder_g = collector

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    pnl_g.set(strategy.realised)          # live numbers
    ladder_g.set(len(strategy.ladders))
    return Response(generate_latest(), media_type="text/plain; charset=utf-8")
