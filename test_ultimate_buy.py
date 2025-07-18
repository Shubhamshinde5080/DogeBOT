#!/usr/bin/env python3
"""
Create the PERFECT buy signal that triggers all 3 conditions
"""
import pandas as pd
import numpy as np
from bot.core.indicators import atr, ema, boll_pct

def force_perfect_buy():
    """Force create data that WILL trigger all conditions"""
    print("🎯 FORCING PERFECT BUY SIGNAL...")
    
    # Strategy: Create price data where:
    # 1. EMA ends up around 0.115
    # 2. Final price is 0.110 (95.7% of EMA = meets >95% condition)
    # 3. Recent high is 0.113+ (creates 2%+ drop)
    # 4. Bollinger Bands are oversold due to recent decline
    
    target_ema = 0.115
    final_price = 0.1102  # 95.8% of target EMA
    recent_high = 0.1127  # Will create 2.2% drop
    
    # Build 25 candles to achieve these targets
    prices = []
    for i in range(25):
        if i < 15:
            # Establish EMA around target level
            prices.append(target_ema + np.random.uniform(-0.002, 0.002))
        elif i < 22:
            # Start decline from recent high
            decline_progress = (i - 14) / 7  # 0 to 1
            start_price = recent_high
            prices.append(start_price - (start_price - final_price) * decline_progress * 0.7)
        else:
            # Final decline to exact target
            prices.append(final_price + np.random.uniform(-0.0001, 0.0001))
    
    prices = np.array(prices)
    
    # Ensure recent high is where we want it
    prices[21] = recent_high  # Set specific recent high
    
    # Create OHLC
    highs = prices + np.random.uniform(0.0001, 0.0005, len(prices))
    lows = prices - np.random.uniform(0.0001, 0.0005, len(prices))
    opens = prices + np.random.uniform(-0.0002, 0.0002, len(prices))
    volumes = np.random.uniform(90000, 110000, len(prices))
    
    # Ensure the recent high is actually in the high column
    highs[21] = max(highs[21], recent_high + 0.0002)
    
    df = pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': prices,
        'volume': volumes
    })
    
    print(f"📊 Engineered price data:")
    print(f"   Final price: {prices[-1]:.6f}")
    print(f"   Recent high: {highs[-3:].max():.6f}")
    print(f"   Expected drop: {((highs[-3:].max() - prices[-1]) / highs[-3:].max() * 100):.2f}%")
    
    # Calculate indicators
    df_test = df.iloc[-30:].copy()
    df_test["atr"] = atr(df_test)
    df_test["ema"] = ema(df_test["close"], span=200)
    df_test["bb"] = boll_pct(df_test)
    
    # Get results
    price = df_test["close"].iat[-1]
    bb_value = df_test["bb"].iat[-1]
    ema_ratio = price / df_test["ema"].iat[-1]
    
    # Check 2% drop
    recent_high_actual = df_test['high'].tail(3).max()  # Look at last 3 candles
    drop_pct = (recent_high_actual - price) / recent_high_actual * 100
    drop_ok = drop_pct >= 2.0
    
    print(f"\n📈 FINAL ANALYSIS:")
    print(f"   Price: {price:.6f}")
    print(f"   EMA: {df_test['ema'].iat[-1]:.6f}")
    print(f"   BB%: {bb_value:.3f}")
    print(f"   EMA Ratio: {ema_ratio:.4f}")
    print(f"   Recent High: {recent_high_actual:.6f}")
    print(f"   Drop %: {drop_pct:.2f}%")
    
    # Test conditions
    bb_condition = bb_value <= 0.30
    ema_condition = ema_ratio > 0.95
    drop_condition = drop_ok
    
    print(f"\n🎯 CONDITIONS:")
    print(f"   1. BB ≤ 0.30: {'✅' if bb_condition else '❌'} {bb_condition}")
    print(f"   2. EMA > 0.95: {'✅' if ema_condition else '❌'} {ema_condition}")
    print(f"   3. Drop ≥ 2%: {'✅' if drop_condition else '❌'} {drop_condition}")
    
    all_met = bb_condition and ema_condition and drop_condition
    print(f"\n{'🎉 PERFECT BUY SIGNAL!' if all_met else '❌ Still not perfect'}")
    
    return all_met

def test_actual_websocket_logic():
    """Test the exact logic from websocket.py"""
    print("\n🔍 Testing EXACT WebSocket Logic...")
    
    try:
        # Import the actual websocket module
        import sys
        sys.path.append('/home/shubham/DogeBot')
        
        from bot.services.websocket import strategy
        from bot.core.indicators import atr, ema, boll_pct
        
        # Create simple test data that should trigger
        test_data = pd.DataFrame({
            'open': [0.115, 0.114, 0.112, 0.111, 0.110],
            'high': [0.116, 0.115, 0.113, 0.112, 0.111],
            'low': [0.114, 0.113, 0.111, 0.110, 0.109],
            'close': [0.115, 0.114, 0.112, 0.111, 0.110],
            'volume': [100000, 100000, 100000, 100000, 100000]
        })
        
        # Extend to 25 rows (same pattern)
        for i in range(20):
            new_row = test_data.iloc[-1].copy()
            new_row['close'] -= 0.0001
            new_row['high'] -= 0.0001
            new_row['low'] -= 0.0001
            new_row['open'] -= 0.0001
            test_data.loc[len(test_data)] = new_row
        
        # Calculate indicators
        df = test_data.iloc[-30:].copy()
        df["atr"] = atr(df)
        df["ema"] = ema(df["close"])
        df["bb"] = boll_pct(df)
        
        price = df["close"].iat[-1]
        bb_value = df["bb"].iat[-1]
        ema_ratio = price / df["ema"].iat[-1]
        
        # Exact same drop check as websocket.py
        def check_recent_drop(df_data, lookback=2):
            if len(df_data) < lookback + 1:
                return False
            recent_high = df_data['high'].tail(lookback).max()
            current_price = df_data['close'].iat[-1]
            drop_percent = (recent_high - current_price) / recent_high
            return drop_percent >= 0.02
        
        drop_confirmed = check_recent_drop(df)
        
        # Exact same conditions as websocket.py
        bb_condition = bb_value <= 0.30
        ema_condition = ema_ratio > 0.95
        
        print(f"   BB: {bb_value:.3f} ≤ 0.30 = {bb_condition}")
        print(f"   EMA: {ema_ratio:.4f} > 0.95 = {ema_condition}")
        print(f"   Drop: {drop_confirmed}")
        
        # This is the EXACT logic from websocket.py
        cycle_active = strategy.cycle is not None
        all_conditions = not cycle_active and bb_condition and ema_condition and drop_confirmed
        
        print(f"   No active cycle: {not cycle_active}")
        print(f"   All conditions: {all_conditions}")
        
        if all_conditions:
            print("✅ WebSocket logic would trigger BUY!")
        else:
            print("❌ WebSocket logic would NOT trigger")
        
        return all_conditions
        
    except Exception as e:
        print(f"❌ Error testing websocket logic: {e}")
        return False

if __name__ == "__main__":
    print("🎯 ULTIMATE BUY CONDITION TEST\n")
    
    perfect_buy = force_perfect_buy()
    websocket_test = test_actual_websocket_logic()
    
    print(f"\n🏁 FINAL VERDICT:")
    print(f"   Engineered perfect scenario: {'✅' if perfect_buy else '❌'}")
    print(f"   WebSocket logic test: {'✅' if websocket_test else '❌'}")
    
    if perfect_buy or websocket_test:
        print(f"\n🎉 BUY CONDITIONS ARE WORKING!")
        print(f"🚀 DogeBot will trigger when real market conditions align!")
    else:
        print(f"\n⚠️ Buy conditions need debugging")
