#!/usr/bin/env python3
"""
Enhanced DogeBot Simulation - More Realistic Market Scenarios
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.append('/home/shubham/DogeBot')
from bot.core.indicators import atr, ema, boll_pct
from bot.core.strategy import GridStrategy

class MockOrderMgr:
    def __init__(self, symbol="DOGEFDUSD"):
        self.symbol = symbol
        self.orders = []
    
    def post_limit_maker(self, side, price, qty):
        self.orders.append({"side": side, "price": price, "qty": qty})
        print(f"    🔥 TRADE: {side} {qty} @ {price:.6f}")
        return {"orderId": len(self.orders)}

def create_realistic_scenario():
    """Create a realistic scenario that should trigger all conditions"""
    
    base_price = 0.21200
    
    # Create 30 candles with realistic DOGE price action
    # Simulate a consolidation followed by a pullback that creates perfect entry
    
    prices = []
    
    # Initial base period (15 candles for indicators)
    for i in range(15):
        noise = np.random.uniform(-0.002, 0.002)
        prices.append(base_price + noise)
    
    # Gradual uptrend (5 candles) - establishes EMA > 95% condition
    for i in range(5):
        trend_price = base_price * (1.01 + i * 0.002)  # Gentle upward trend
        noise = np.random.uniform(-0.001, 0.001)
        prices.append(trend_price + noise)
    
    # Small rally then pullback (10 candles) - creates 2% drop + low BB
    rally_high = base_price * 1.025  # 2.5% above base
    
    # Rally phase (3 candles)
    prices.extend([
        base_price * 1.015,
        base_price * 1.020,
        rally_high,  # High point
    ])
    
    # Pullback phase (7 candles) - gradual decline
    decline_steps = np.linspace(rally_high, base_price * 0.995, 7)
    prices.extend(decline_steps)
    
    return prices

def test_realistic_market():
    """Test with realistic market data that should trigger"""
    
    print("🎯 REALISTIC MARKET SIMULATION")
    print("=" * 50)
    
    # Create realistic price data
    prices = create_realistic_scenario()
    
    # Build dataframe
    df = pd.DataFrame({
        'open': prices,
        'high': [p * 1.0015 for p in prices],  # Small wicks
        'low': [p * 0.9985 for p in prices],
        'close': prices,
        'volume': [1000000 + np.random.randint(-100000, 100000) for _ in prices]
    })
    
    print(f"📊 Market Data Overview:")
    print(f"   Total candles: {len(df)}")
    print(f"   Price range: {df['close'].min():.6f} - {df['close'].max():.6f}")
    print(f"   Latest price: {df['close'].iloc[-1]:.6f}")
    
    # Calculate indicators
    df['atr'] = atr(df)
    df['ema'] = ema(df['close'])
    df['bb'] = boll_pct(df)
    
    # Get latest values
    latest_price = df['close'].iloc[-1]
    latest_atr = df['atr'].iloc[-1]
    latest_bb = df['bb'].iloc[-1]
    latest_ema = df['ema'].iloc[-1]
    
    # Check 2% drop
    def check_recent_drop(df_data, lookback=3):  # Check last 3 candles
        if len(df_data) < lookback + 1:
            return False, 0
        recent_high = df_data['high'].tail(lookback + 1).max()
        current_price = df_data['close'].iloc[-1]
        drop_percent = (recent_high - current_price) / recent_high
        return drop_percent >= 0.02, drop_percent
    
    drop_confirmed, drop_pct = check_recent_drop(df)
    
    print(f"\n📈 Technical Analysis:")
    print(f"   Price: {latest_price:.6f}")
    print(f"   ATR: {latest_atr:.6f}")
    print(f"   EMA: {latest_ema:.6f}")
    print(f"   BB%: {latest_bb:.3f}")
    print(f"   EMA Ratio: {latest_price/latest_ema:.4f}")
    print(f"   Drop: {drop_pct:.1%} ({'✅' if drop_confirmed else '❌'})")
    
    # Test all conditions
    conditions = {
        "Data (≥10)": len(df) >= 10,
        "ATR Valid": not pd.isna(latest_atr),
        "BB ≤ 0.30": latest_bb <= 0.30,
        "EMA > 95%": latest_price > 0.95 * latest_ema,
        "2% Drop": drop_confirmed,
        "No Cycle": True  # Assume no active cycle
    }
    
    print(f"\n🎯 Condition Check:")
    for condition, result in conditions.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {condition}: {status}")
    
    all_met = all(conditions.values())
    
    if all_met:
        print(f"\n🚀 PERFECT! All conditions met - Bot would start trading!")
        
        # Simulate strategy activation
        mock_order_mgr = MockOrderMgr()
        strategy = GridStrategy(order_mgr=mock_order_mgr)
        
        print(f"\n🎮 Simulating Strategy Activation:")
        strategy.start_cycle(latest_price, latest_atr)
        
        print(f"   Entry Price: {latest_price:.6f}")
        print(f"   Step Size: {strategy.step:.6f}")
        print(f"   Next Buy: {strategy.next_buy:.6f}")
        print(f"   Quantity: {strategy.qty_next}")
        
        # Simulate a price drop to trigger first buy
        trigger_price = strategy.next_buy
        print(f"\n💡 If price drops to {trigger_price:.6f}:")
        strategy.on_tick(trigger_price, latest_atr)
        
    else:
        failed_conditions = [name for name, result in conditions.items() if not result]
        print(f"\n⏳ Missing conditions: {', '.join(failed_conditions)}")
        
        # Show how close we are
        if not conditions["BB ≤ 0.30"]:
            print(f"   BB needs to drop from {latest_bb:.3f} to ≤0.30")
        if not conditions["EMA > 95%"]:
            ratio = latest_price / latest_ema
            print(f"   EMA ratio is {ratio:.4f}, needs >0.95")
        if not conditions["2% Drop"]:
            print(f"   Drop is only {drop_pct:.1%}, needs ≥2%")
    
    return all_met

if __name__ == "__main__":
    # Run multiple simulations to find a working scenario
    print("🔄 Running multiple realistic scenarios...")
    print()
    
    success_count = 0
    for i in range(5):
        print(f"🎲 Simulation {i+1}:")
        print("-" * 30)
        
        success = test_realistic_market()
        if success:
            success_count += 1
            print("✅ SUCCESS!")
        else:
            print("❌ Conditions not met")
        print()
    
    print(f"📊 SUMMARY: {success_count}/5 simulations triggered trading")
    
    if success_count > 0:
        print("🎉 Bot logic is working - it CAN trigger under right conditions!")
    else:
        print("⚠️  All simulations failed - conditions may be too restrictive")
