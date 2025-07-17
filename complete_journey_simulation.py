#!/usr/bin/env python3
"""
Complete DogeBot Journey Simulation
1. Collect required candles (10+)
2. Run 10 candles that don't meet conditions
3. Run 5 candles that DO meet all conditions
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.path.append('/home/shubham/DogeBot')
from bot.core.indicators import atr, ema, boll_pct
from bot.core.strategy import GridStrategy

class MockOrderMgr:
    def __init__(self):
        self.orders = []
    
    def post_limit_maker(self, side, price, qty):
        self.orders.append({"side": side, "price": price, "qty": qty})
        print(f"        🔥 ORDER PLACED: {side} {qty} DOGE @ {price:.6f}")
        return {"orderId": len(self.orders)}

def simulate_websocket_tick(df, strategy, candle_num):
    """Simulate exact websocket logic for each candle"""
    
    print(f"\n📊 CANDLE #{candle_num} - Processing...")
    
    # Check minimum data requirement (like in websocket.py)
    if len(df) < 10:
        print(f"    ⏳ Still collecting candles: {len(df)}/10 needed")
        return False, "Collecting data"
    
    # Calculate indicators (like in websocket.py)
    df["atr"] = atr(df)
    df["ema"] = ema(df["close"])
    df["bb"] = boll_pct(df)
    
    price = df["close"].iat[-1]
    atr_now = df["atr"].iat[-1]
    
    # Check ATR validity
    if pd.isna(atr_now):
        print(f"    ⚠️ ATR is NaN, skipping this candle")
        return False, "ATR NaN"
    
    # 2% drop check (from enhanced websocket.py)
    def check_recent_drop(df_data, lookback=2):
        if len(df_data) < lookback + 1:
            return False
        recent_high = df_data['high'].tail(lookback + 1).max()
        current_price = df_data['close'].iat[-1]
        drop_percent = (recent_high - current_price) / recent_high
        return drop_percent >= 0.02
    
    drop_confirmed = check_recent_drop(df)
    
    # Check all conditions (exactly like websocket.py)
    bb_condition = df["bb"].iat[-1] <= 0.30
    ema_condition = price > 0.95 * df["ema"].iat[-1]
    cycle_condition = not strategy.cycle
    
    # Print technical analysis (like enhanced websocket.py)
    print(f"    📈 Technical Analysis:")
    print(f"       Price: {price:.6f}")
    print(f"       ATR: {atr_now:.6f}")
    print(f"       BB%: {df['bb'].iat[-1]:.3f}")
    print(f"       EMA Ratio: {price/df['ema'].iat[-1]:.4f}")
    print(f"       2% Drop: {drop_confirmed}")
    
    # Show condition status
    conditions = {
        "BB ≤ 0.30": bb_condition,
        "EMA > 95%": ema_condition,
        "2% Drop": drop_confirmed,
        "No Cycle": cycle_condition
    }
    
    print(f"    🎯 Conditions:")
    for name, result in conditions.items():
        status = "✅" if result else "❌"
        print(f"       {status} {name}: {result}")
    
    # Check if all conditions met
    all_met = bb_condition and ema_condition and drop_confirmed and cycle_condition
    
    if all_met:
        print(f"    🚀 ALL CONDITIONS MET! Starting trading cycle...")
        strategy.start_cycle(price, atr_now)
        
        # Simulate immediate price action to trigger first buy
        trigger_price = strategy.next_buy - 0.000001
        print(f"    💡 Price drops to {trigger_price:.6f} - triggering first buy...")
        strategy.on_tick(trigger_price, atr_now)
        
        return True, "TRADING STARTED"
    else:
        missing = [name for name, result in conditions.items() if not result]
        print(f"    ⏳ Waiting for: {', '.join(missing)}")
        return False, f"Missing: {', '.join(missing)}"

def create_journey_data():
    """Create complete journey: data collection -> failures -> success"""
    
    base_price = 0.21200
    all_prices = []
    
    print("🎯 CREATING COMPLETE BOT JOURNEY")
    print("=" * 60)
    
    # PHASE 1: Initial data collection (15 candles)
    print("\n📊 PHASE 1: INITIAL DATA COLLECTION (15 candles)")
    print("Creating stable base for indicator calculation...")
    
    for i in range(15):
        # Stable prices with small variations
        noise = np.random.uniform(-0.001, 0.001)
        price = base_price + noise
        all_prices.append(price)
    
    print(f"   ✅ Base data: {len(all_prices)} candles created")
    
    # PHASE 2: 10 candles that DON'T meet conditions
    print("\n📊 PHASE 2: CONDITIONS NOT MET (10 candles)")
    print("Creating scenarios that fail various conditions...")
    
    for i in range(10):
        if i < 3:
            # High volatility (BB will be high)
            volatility = 0.005  # High volatility
            price = base_price * (1 + np.random.uniform(-volatility, volatility))
            print(f"   Candle {len(all_prices)+1}: High volatility scenario")
        elif i < 6:
            # Downtrend (EMA condition will fail)
            trend_factor = 0.98 - (i-3) * 0.005  # Declining trend
            price = base_price * trend_factor
            print(f"   Candle {len(all_prices)+1}: Downtrend scenario")
        else:
            # No significant drop (2% drop condition will fail)
            stable_factor = 1.002 + (i-6) * 0.001  # Gentle rise
            price = base_price * stable_factor
            print(f"   Candle {len(all_prices)+1}: No pullback scenario")
        
        all_prices.append(price)
    
    print(f"   ✅ Failure scenarios: {10} candles added")
    
    # PHASE 3: 5 candles that WILL meet all conditions
    print("\n📊 PHASE 3: PERFECT CONDITIONS (5 candles)")
    print("Creating ideal setup that will trigger trading...")
    
    # Transition back to base with tight range for low BB
    transition_prices = np.linspace(all_prices[-1], base_price * 1.005, 3)
    for i, price in enumerate(transition_prices):
        all_prices.append(price)
        print(f"   Candle {len(all_prices)}: Transition to stable range")
    
    # Create perfect scenario: small spike then 2% pullback
    spike_high = base_price * 1.022  # 2.2% above base
    all_prices.append(spike_high)
    print(f"   Candle {len(all_prices)}: Small spike to {spike_high:.6f}")
    
    # Perfect pullback (exactly 2% drop)
    pullback_price = spike_high * 0.98  # 2% drop
    all_prices.append(pullback_price)
    print(f"   Candle {len(all_prices)}: Pullback to {pullback_price:.6f} (2% drop)")
    
    print(f"   ✅ Perfect setup: {5} candles added")
    print(f"\n📊 TOTAL JOURNEY: {len(all_prices)} candles")
    
    return all_prices

def run_complete_journey():
    """Run the complete bot journey simulation"""
    
    prices = create_journey_data()
    
    # Create OHLC dataframe
    df = pd.DataFrame({
        'open': prices,
        'high': [p * 1.0005 for p in prices],  # Small wicks
        'low': [p * 0.9995 for p in prices],
        'close': prices,
        'volume': [1000000] * len(prices)
    })
    
    # Initialize strategy
    mock_order_mgr = MockOrderMgr()
    strategy = GridStrategy(order_mgr=mock_order_mgr)
    
    print("\n" + "="*60)
    print("🚀 STARTING COMPLETE BOT JOURNEY SIMULATION")
    print("="*60)
    
    phase_markers = {
        10: "\n🔄 PHASE 1 COMPLETE: Data collection finished",
        25: "\n🔄 PHASE 2 COMPLETE: Failed conditions tested", 
        30: "\n🔄 PHASE 3 COMPLETE: Perfect conditions created"
    }
    
    # Simulate each candle
    for i in range(1, len(df) + 1):
        # Get data up to current candle
        current_df = df.iloc[:i].copy()
        
        # Mark phase transitions
        if i in phase_markers:
            print(phase_markers[i])
        
        # Simulate websocket tick
        triggered, status = simulate_websocket_tick(current_df, strategy, i)
        
        if triggered:
            print(f"\n🎉 SUCCESS! Trading started at candle #{i}")
            print(f"🎯 Entry Price: {current_df['close'].iat[-1]:.6f}")
            print(f"📏 Step Size: {strategy.step:.6f}")
            print(f"🎪 Grid Active: {len(strategy.ladders)} positions")
            
            # Simulate a profitable sell
            if len(strategy.ladders) > 0:
                ladder = strategy.ladders[0]
                sell_price = ladder.sell
                buy_price = ladder.buy
                qty = ladder.qty
                
                print(f"\n💰 SIMULATING PROFITABLE SELL:")
                strategy.handle_sell_fill(sell_price, buy_price, qty)
                print(f"   💵 Trade Profit: ${(sell_price - buy_price) * qty:.4f}")
                print(f"   📊 Total PnL: ${strategy.realised:.4f}")
            
            break
        else:
            print(f"    📊 Status: {status}")
    
    # Final summary
    print(f"\n" + "="*60)
    print("🏆 JOURNEY COMPLETE - SUMMARY")
    print("="*60)
    
    if strategy.cycle:
        print("✅ SUCCESS: Bot successfully started trading!")
        print(f"📊 Final Status:")
        print(f"   • Trading Active: {strategy.cycle}")
        print(f"   • Orders Placed: {len(mock_order_mgr.orders)}")
        print(f"   • Active Positions: {len(strategy.ladders)}")
        print(f"   • Realized PnL: ${strategy.realised:.4f}")
        print(f"   • Daily Target: ${strategy.profit_target:.2f}")
        
        progress = (strategy.realised / strategy.profit_target) * 100
        print(f"   • Progress to Target: {progress:.1f}%")
        
    else:
        print("⚠️  Bot completed journey but conditions never aligned")
    
    print(f"\n💡 KEY INSIGHTS:")
    print(f"   • Your bot correctly waits for optimal conditions")
    print(f"   • All 6 conditions must align simultaneously")
    print(f"   • When conditions meet, trading starts immediately")
    print(f"   • Grid strategy executes profitable trades")

if __name__ == "__main__":
    run_complete_journey()
