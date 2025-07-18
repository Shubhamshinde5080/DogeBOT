from dataclasses import dataclass, field
from datetime import datetime
import logging
from binance.spot import Spot
import os, time

logger = logging.getLogger(__name__)
TICK = 0.00001

@dataclass
class OrderMgr:
    symbol: str = "DOGEFDUSD"  # Your actual trading pair
    client: Spot = None
    events: list = field(default_factory=list)
    
    def __post_init__(self):
        if self.client is None:
            # Support both Railway.app and local environment variable names
            api_key = os.getenv("BINANCE_API_KEY") or os.getenv("API_KEY")
            api_secret = os.getenv("BINANCE_API_SECRET") or os.getenv("API_SECRET")
            base_url = os.getenv("BINANCE_BASE_URL") or os.getenv("BASE_URL", "https://testnet.binance.vision")
            
            self.client = Spot(
                api_key=api_key,
                api_secret=api_secret,
                base_url=base_url)

    def post_limit_maker(self, side: str, price: float, qty: float):
        price = round(price/TICK)*TICK
        logger.info(f"🔨 Placing {side.upper()} – price={price:.6f}, qty={qty}")
        
        try:
            resp = self.client.new_order(
                symbol=self.symbol,
                side=side,
                type="LIMIT_MAKER",
                price=f"{price:.5f}",
                quantity=f"{qty:.0f}",
                newOrderRespType="RESULT")
            
            # Log successful order
            if "fills" in resp and resp["fills"]:
                filled_price = float(resp["fills"][0]["price"])
                logger.info(f"✅ {side.upper()} filled – price={filled_price:.6f}, qty={qty}")
            else:
                logger.info(f"📋 {side.upper()} order placed – price={price:.6f}, qty={qty}")
            
            # Record event
            self.events.append({
                "time": datetime.utcnow().isoformat(),
                "action": side.upper(),
                "price": price,
                "qty": qty,
            })
            
            return resp
            
        except Exception as e:
            if "match and take" in str(e):
                offset = -TICK if side == "BUY" else TICK
                logger.warning(f"⚠️ Order would match, adjusting price by {offset}")
                time.sleep(0.05)
                return self.post_limit_maker(side, price+offset, qty)
            else:
                logger.error(f"❌ Order failed: {e}")
                raise

    def cancel_order(self, order_id):
        """Cancel an order by ID"""
        try:
            resp = self.client.cancel_order(
                symbol=self.symbol,
                orderId=order_id
            )
            logger.info(f"🗑️ Order cancelled – ID={order_id}")
            return resp
        except Exception as e:
            logger.error(f"❌ Cancel order failed: {e}")
            return None