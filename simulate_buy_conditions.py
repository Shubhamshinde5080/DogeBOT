#!/usr/bin/env python3
"""
DogeBot Buy Conditions Simulator
Creates realistic market scenarios to test if bot triggers correctly
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add bot path
sys.path.append('/home/shubham/DogeBot')

from bot.core.indicators import atr, ema, boll_pct
from bot.core.strategy import GridStrategy
from bot.core.order_mgr import OrderMgr

class MockOrderMgr:
    """Mock order manager for testing"""
    def __init__(self, symbol="DOGEFDUSD"):
        self.symbol = symbol
        self.orders = []
    
    def post_limit_maker(self, side, price, qty):
        order = {"side": side, "price": price, "qty": qty, "time": datetime.now()}
        self.orders.append(order)
        print(f"    📋 MOCK ORDER: {side} {qty} {self.symbol} @ {price:.6f}")
        return {"orderId": len(self.orders)}

def create_market_scenario(scenario_name, base_price=0.21200):
    """Create different market scenarios for testing"""
    
    # Create 25 candles for proper indicator calculation (ATR needs 14, BB needs 20)
    base_sequence = [
        base_price * 0.990, base_price * 0.992, base_price * 0.995,
        base_price * 0.997, base_price * 0.999, base_price * 1.001,
        base_price * 1.003, base_price * 1.005, base_price * 1.002,
        base_price * 1.000, base_price * 0.998, base_price * 1.004,
        base_price * 1.001, base_price * 0.999, base_price * 1.002,  # 15 candles for ATR
    ]
    
    scenarios = {
        "Perfect_Entry": {
            "description": "BB oversold, uptrend, 2% drop - SHOULD TRIGGER",
            "prices": base_sequence + [
                base_price * 1.025,  # Start higher for 2% drop
                base_price * 1.020,  # Small decline
                base_price * 1.015,  # Continued decline
                base_price * 1.010,  # More decline
                base_price * 1.005,  # Almost at base
                base_price * 1.000,  # At base (2.5% drop from high)
                base_price * 0.998,  # Slight overshoot (low BB)
                base_price * 0.996,  # More overshoot (very low BB)
                base_price * 0.995,  # Bottom (should be oversold)
                base_price * 1.001,  # Small recovery - trigger point
            ]
        },
        
        "No_Drop": {
            "description": "Good BB & EMA but no 2% drop - SHOULD NOT TRIGGER", 
            "prices": base_sequence + [
                base_price * 0.995,  # Start low (good BB)
                base_price * 0.996,  # Tiny rise
                base_price * 0.997,  # More rise
                base_price * 0.998,  # Continued
                base_price * 0.999,  # Almost base
                base_price * 1.000,  # Base price
                base_price * 1.001,  # Small rise (no 2% drop)
                base_price * 1.002,  # More rise
                base_price * 1.003,  # Rising trend
                base_price * 1.004,  # Current (steady rise, no drop)
            ]
        },
        
        "Downtrend": {
            "description": "2% drop but price below EMA - SHOULD NOT TRIGGER",
            "prices": base_sequence + [
                base_price * 1.050,  # High starting point
                base_price * 1.030,  # Decline
                base_price * 1.010,  # More decline
                base_price * 0.990,  # Below EMA
                base_price * 0.970,  # Further below
                base_price * 0.950,  # Deep decline
                base_price * 0.940,  # Deeper
                base_price * 0.930,  # Even deeper
                base_price * 0.925,  # Very low
                base_price * 0.920,  # Current (>2% drop but strong downtrend)
            ]
        },
        
        "High_Volatility": {
            "description": "2% drop, uptrend but BB > 0.30 - SHOULD NOT TRIGGER",
            "prices": base_sequence + [
                base_price * 1.000,  # Base
                base_price * 1.050,  # Big jump (high volatility)
                base_price * 0.980,  # Big drop
                base_price * 1.040,  # Big jump again
                base_price * 0.990,  # Drop again
                base_price * 1.030,  # Volatile moves (wide BB)
                base_price * 1.005,  # Back near base
                base_price * 1.020,  # Up again
                base_price * 0.995,  # Drop (2%+ from recent high)
                base_price * 1.010,  # Current (volatile market, high BB)
            ]
        }
    }
    
    return scenarios.get(scenario_name, scenarios["Perfect_Entry"])

def simulate_websocket_logic(df, strategy):
    """Simulate the exact websocket logic from your bot"""
    
    if len(df) < 10:
        return False, "❌ Insufficient data (need 10+ candles)"
    
    # Calculate indicators exactly like in websocket.py
    df["atr"] = atr(df)
    df["ema"] = ema(df["close"])  
    df["bb"] = boll_pct(df)
    
    price = df["close"].iat[-1]
    atr_now = df["atr"].iat[-1]
    
    if pd.isna(atr_now):
        return False, "❌ ATR is NaN"
    
    # 2% drop check (from enhanced code)
    def check_recent_drop(df_data, lookback=2):
        if len(df_data) < lookback + 1:
            return False
        recent_high = df_data['high'].tail(lookback + 1).max()
        current_price = df_data['close'].iat[-1]
        drop_percent = (recent_high - current_price) / recent_high
        return drop_percent >= 0.02
    
    drop_confirmed = check_recent_drop(df)
    
    # Check all conditions like in websocket.py
    bb_condition = df["bb"].iat[-1] <= 0.30
    ema_condition = price > 0.95 * df["ema"].iat[-1]
    cycle_condition = not strategy.cycle
    
    # Print detailed analysis
    print(f"    📊 Technical Analysis:")
    print(f"       Price: {price:.6f}")
    print(f"       ATR: {atr_now:.6f}")
    print(f"       BB%: {df['bb'].iat[-1]:.3f} (need ≤0.30)")
    print(f"       EMA Ratio: {price/df['ema'].iat[-1]:.4f} (need >0.95)")
    print(f"       2% Drop: {drop_confirmed}")
    
    # Condition results
    conditions = {
        "Data": len(df) >= 10,
        "ATR": not pd.isna(atr_now),
        "BB": bb_condition,
        "EMA": ema_condition, 
        "Drop": drop_confirmed,
        "Cycle": cycle_condition
    }
    
    print(f"    🎯 Conditions:")
    for name, result in conditions.items():
        status = "✅" if result else "❌"
        print(f"       {status} {name}: {result}")
    
    all_met = all(conditions.values())
    
    if all_met:
        # Simulate starting cycle
        strategy.start_cycle(price, atr_now)
        return True, "🎯 ALL CONDITIONS MET - TRADE TRIGGERED!"
    else:
        missing = [name for name, result in conditions.items() if not result]
        return False, f"⏳ Waiting for: {', '.join(missing)}"

def run_simulation():
    """Run comprehensive simulation of all scenarios"""
    
    print("🎮 DOGEBOT BUY CONDITIONS SIMULATION")
    print("=" * 70)
    print("Testing realistic market scenarios to verify bot logic...")
    print()
    
    scenarios = ["Perfect_Entry", "No_Drop", "Downtrend", "High_Volatility"]
    results = {}
    
    for scenario_name in scenarios:
        print(f"📊 SCENARIO: {scenario_name}")
        print("-" * 50)
        
        # Create market data
        scenario = create_market_scenario(scenario_name)
        print(f"Description: {scenario['description']}")
        print()
        
        # Build OHLC dataframe
        prices = scenario['prices']
        df = pd.DataFrame({
            'open': prices,
            'high': [p * 1.001 for p in prices],  # Small wick up
            'low': [p * 0.999 for p in prices],   # Small wick down  
            'close': prices,
            'volume': [1000000] * len(prices)     # Constant volume
        })
        
        # Create mock strategy
        mock_order_mgr = MockOrderMgr()
        strategy = GridStrategy(order_mgr=mock_order_mgr)
        
        # Run simulation
        triggered, message = simulate_websocket_logic(df, strategy)
        results[scenario_name] = triggered
        
        print(f"    🎯 RESULT: {message}")
        
        if triggered:
            print(f"    🔥 GRID ACTIVATED!")
            print(f"       Entry Price: {df['close'].iat[-1]:.6f}")
            print(f"       Step Size: {strategy.step:.6f}")
            print(f"       First Buy: {strategy.next_buy:.6f}")
        
        print()
    
    # Summary
    print("📋 SIMULATION SUMMARY")
    print("=" * 30)
    
    expected_results = {
        "Perfect_Entry": True,   # Should trigger
        "No_Drop": False,        # Should not trigger
        "Downtrend": False,      # Should not trigger  
        "High_Volatility": False # Should not trigger
    }
    
    all_correct = True
    for scenario, expected in expected_results.items():
        actual = results[scenario]
        correct = actual == expected
        status = "✅ CORRECT" if correct else "❌ WRONG"
        print(f"{scenario}: Expected {expected}, Got {actual} - {status}")
        if not correct:
            all_correct = False
    
    print()
    if all_correct:
        print("🎉 ALL TESTS PASSED! Bot logic is working correctly!")
        print("🚀 Your bot will only trade in optimal conditions!")
    else:
        print("⚠️  Some tests failed - bot logic needs adjustment")
    
    return results

if __name__ == "__main__":
    run_simulation()
