import os, json, asyncio, pandas as pd, logging
from datetime import datetime, date
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
from bot.core.strategy import GridStrategy
from bot.core.order_mgr import OrderMgr
from bot.core.indicators import atr, ema, boll_pct

# Global configuration
DAILY_TARGET = float(os.getenv("DAILY_TARGET", 6.0))
_last_target_date: date = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/dogebot_websocket.log')
    ]
)
logger = logging.getLogger(__name__)

SYMBOL  = "DOGEFDUSD"  # Your actual trading pair
# read from .env so you can flip to live later
IS_TEST = "testnet" in os.getenv("BASE_URL", "")

# ------------ 1.  point to the correct stream URL -------------
# Note: Binance testnet doesn't have a separate WebSocket endpoint for market data
# Use the live WebSocket for market data even when trading on testnet
STREAM_URL = "wss://stream.binance.com:9443/ws"

# Initialize components  
order_mgr = OrderMgr(symbol=SYMBOL)  # Explicitly pass the symbol to match
strategy  = GridStrategy(order_mgr=order_mgr)

bars = pd.DataFrame(columns=["open", "high", "low", "close"])

# ------------ 2.  message handlers -------------------------------
def handle_kline(_, raw_msg: str):
    """Handle incoming kline messages from WebSocket"""
    global _last_target_date
    now = datetime.utcnow()
    
    # Log all messages for debugging
    logger.debug(f"🔍 Raw WebSocket message: {raw_msg[:200]}...")
    
    # reset at midnight UTC
    if _last_target_date != now.date():
        strategy.realised = 0.0
        _last_target_date = now.date()
        logger.info(f"🌄 New day reset – realised PnL cleared")

    # pause trading if daily target met
    if strategy.realised >= DAILY_TARGET:
        logger.info(f"🎯 Daily target ${DAILY_TARGET:.2f} reached – waiting for tomorrow")
        return
        logger.info(f"🎯 Daily target ${DAILY_TARGET:.2f} reached – waiting for tomorrow")
        return

    try:
        data = json.loads(raw_msg)
        
        # Spot WS sends an ACK first: {"result":null}
        if "k" not in data:
            return
            
        kline_data = data["k"]
        
        # Ignore inflight candles; wait until it closes
        if not kline_data["x"]:  # "x" == candle_is_closed
            return
        
        # Store closed candle data
        idx = pd.to_datetime(kline_data["t"], unit="ms")
        bars.loc[idx, ["open", "high", "low", "close"]] = [
            float(kline_data[x]) for x in ["o", "h", "l", "c"]
        ]
        
        # Prevent unbounded growth - keep only last 500 bars
        if len(bars) > 500:
            bars.drop(bars.index[:-250], inplace=True)
        
        # Log first successful closed candle
        if len(bars) == 1:
            logger.info(f"🎯 First closed kline stored: {kline_data['c']} at {idx}")
        
        logger.info(f"💹 Closed 15-min candle: {kline_data['c']} (#{len(bars)})")
        
        logger.debug(f"📊 Candles collected: {len(bars)}/10 (need 10 for strategy)")

        if len(bars) < 10:
            return

        df = bars.iloc[-30:].copy()
        df["atr"]  = atr(df)
        df["ema"]  = ema(df["close"])
        df["bb"]   = boll_pct(df)

        price   = df["close"].iat[-1]
        atr_now = df["atr"].iat[-1]
        if pd.isna(atr_now):
            return

        if not strategy.cycle:
            logger.info(f"⏳ Waiting – price={price:.6f}, ATR={atr_now:.6f}, BB={df['bb'].iat[-1]:.3f}, EMA_ratio={price/df['ema'].iat[-1]:.4f}")

        # More flexible entry conditions for testing:
        # Original: df["bb"].iat[-1] <= 0.15 and price > 0.97 * df["ema"].iat[-1]
        # Test conditions: More lenient for easier triggering
        bb_condition = df["bb"].iat[-1] <= 0.30  # Increased from 0.15 to 0.30
        ema_condition = price > 0.95 * df["ema"].iat[-1]  # Decreased from 0.97 to 0.95
        
        if not strategy.cycle and bb_condition and ema_condition:
            logger.info(f"🎯 Entry conditions met! BB={df['bb'].iat[-1]:.3f} <= 0.30, Price/EMA={price/df['ema'].iat[-1]:.4f} > 0.95")
            strategy.start_cycle(price, atr_now)

        strategy.on_tick(price, atr_now)
        
        # Optional: Print live price updates
        logger.debug(f"💹 Kline update: {kline_data['c']}")
        
    except Exception as e:
        logger.error(f"❌ Error processing kline data: {e}")
        # Print the raw message for debugging
        logger.debug(f"🔍 Raw message that caused error: {raw_msg[:200]}...")

def handle_error(_, err):
    """Handle WebSocket errors"""
    logger.error(f"❌ WS error: {err}")

# ------------ 3.  async websocket coroutine -----------------------
async def start_websocket():
    """Start the websocket connection with new v3+ API"""
    try:
        logger.info(f"🔌 Connecting to WebSocket: {STREAM_URL}")
        
        # Initialize with handlers in constructor (v3+ API)
        ws = SpotWebsocketStreamClient(
            stream_url=STREAM_URL,
            on_message=handle_kline,
            on_error=handle_error,
        )
        
        logger.info(f"📡 Subscribing to {SYMBOL} 15m klines...")
        # Subscribe without callback parameter (v3+ API)
        ws.kline(symbol=SYMBOL, interval="15m")
        
        logger.info("🎉 WebSocket handshake successful, now listening…")
        
        # keep this async task alive forever (no ws.start() in v3+)
        while True:
            await asyncio.sleep(3600)  # 1 h heartbeat
            
    except Exception as e:
        logger.error(f"❌ WebSocket failed to start: {e}")
        # Retry after delay
        await asyncio.sleep(10)
        logger.info("🔄 Retrying WebSocket connection...")
        await start_websocket()

# Don't auto-start - let it be started manually to avoid startup crashes