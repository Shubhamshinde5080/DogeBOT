import os
import logging
from dataclasses import dataclass, field
from .indicators import vwap

logger = logging.getLogger(__name__)

@dataclass
class Ladder:
    buy: float
    sell: float
    qty: float

@dataclass
class GridStrategy:
    order_mgr: any
    step_mult: float = float(os.getenv("STEP_MULT", 0.25))
    qty0: int = int(os.getenv("QTY0", 300))
    qty_inc: int = int(os.getenv("QTY_INC", 50))
    profit_target: float = float(os.getenv("PROFIT_TARGET", 6))
    fdusd_cap: float = float(os.getenv("FDUSD_CAP", 1100))

    ladders: list = field(default_factory=list)
    realised: float = 0.0
    cycle: bool = False
    step: float = None
    next_buy: float = None
    qty_next: int = None

    def start_cycle(self, price, atr):
        logger.info(f"🔔 ▶️  Cycle START – entry={price:.6f}, ATR={atr:.6f}")
        self.cycle = True
        self.realised = 0
        self.ladders.clear()
        self.step = self.step_mult*atr
        self.qty_next = self.qty0
        self.next_buy = price - self.step

    def on_tick(self, price, atr):
        # fill logic handled by websocket exec reports (see services.websocket)
        # here only ladder placement
        if self.cycle and self.next_buy and price <= self.next_buy and \
           self.funds_free() >= self.next_buy*self.qty_next:
            self.order_mgr.post_limit_maker("BUY", self.next_buy, self.qty_next)
            self.next_buy -= self.step
            self.qty_next += self.qty_inc

    def funds_free(self):
        used = sum(l.buy*l.qty for l in self.ladders)
        return self.fdusd_cap - used

    def handle_buy_fill(self, price, qty):
        self.ladders.append(Ladder(price, price+self.step, qty))
        self.order_mgr.post_limit_maker("SELL", price+self.step, qty)

    def handle_sell_fill(self, price, buy_price, qty):
        self.realised += (price-buy_price)*qty
        self.ladders = [l for l in self.ladders if not (l.buy==buy_price and l.qty==qty)]
        if self.realised >= self.profit_target:
            self.close_all(price)

    def close_all(self, mkt):
        for l in self.ladders:
            self.order_mgr.post_limit_maker("SELL", mkt, l.qty)
        self.ladders.clear()
        self.cycle=False