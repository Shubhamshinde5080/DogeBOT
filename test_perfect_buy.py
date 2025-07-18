#!/usr/bin/env python3
"""
Test that creates a perfect buy scenario to verify all conditions trigger
"""
import pandas as pd
import numpy as np
from bot.core.indicators import atr, ema, boll_pct

def create_perfect_buy_scenario():
    """Create data that will trigger all buy conditions"""
    print("🎯 Creating PERFECT BUY SCENARIO...")
    
    # Create 25 candles with specific pattern:
    # - Start at reasonable price near EMA
    # - Create small decline with 2%+ drop
    # - End up oversold (BB ≤ 0.30) but still near EMA support (> 0.95)
    
    dates = pd.date_range('2025-01-01', periods=25, freq='15min')
    
    # Careful price construction to meet all conditions
    base_ema = 0.115  # Target EMA level
    prices = []
    
    # Build price series that will result in proper EMA and BB levels
    for i in range(25):
        if i < 10:
            # Start slightly above target EMA
            prices.append(base_ema + 0.003 + np.random.uniform(-0.0005, 0.0005))
        elif i < 20:
            # Gradual consolidation around EMA level
            prices.append(base_ema + 0.002 + np.random.uniform(-0.001, 0.001))
        else:
            # Final decline to create oversold + 2% drop but stay near EMA
            decline = (i - 19) * 0.0008  # Small decline
            prices.append(base_ema + 0.0015 - decline + np.random.uniform(-0.0002, 0.0002))
    
    prices = np.array(prices)
    
    # Create OHLC with small spread
    spread = 0.001
    highs = prices + np.random.uniform(0.0002, spread, len(prices))
    lows = prices - np.random.uniform(0.0002, spread, len(prices))
    opens = prices + np.random.uniform(-0.0005, 0.0005, len(prices))
    volumes = np.random.uniform(80000, 120000, len(prices))
    
    df = pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': prices,
        'volume': volumes
    }, index=dates)
    
    print(f"📊 Price range: {df['close'].min():.6f} - {df['close'].max():.6f}")
    
    # Calculate indicators exactly like websocket.py
    df_test = df.iloc[-30:].copy()  # Use last 30 like in websocket
    df_test["atr"] = atr(df_test)
    df_test["ema"] = ema(df_test["close"], span=200)  # 200-period EMA
    df_test["bb"] = boll_pct(df_test)
    
    # Get final values
    price = df_test["close"].iat[-1]
    atr_now = df_test["atr"].iat[-1]
    bb_value = df_test["bb"].iat[-1]
    ema_value = df_test["ema"].iat[-1]
    ema_ratio = price / ema_value
    
    print(f"\n📈 Technical Analysis:")
    print(f"   Current Price: {price:.6f}")
    print(f"   EMA(200): {ema_value:.6f}")
    print(f"   ATR: {atr_now:.6f}")
    print(f"   BB%: {bb_value:.3f}")
    print(f"   EMA Ratio: {ema_ratio:.4f}")
    
    # Test 2% drop (same function as websocket.py)
    def check_recent_drop(df_data, lookback=2):
        if len(df_data) < lookback + 1:
            return False
        recent_high = df_data['high'].tail(lookback).max()
        current_price = df_data['close'].iat[-1]
        drop_percent = (recent_high - current_price) / recent_high
        return drop_percent >= 0.02
    
    drop_confirmed = check_recent_drop(df_test)
    recent_high = df_test['high'].tail(2).max()
    drop_pct = (recent_high - price) / recent_high * 100
    
    print(f"   Recent High: {recent_high:.6f}")
    print(f"   Drop %: {drop_pct:.2f}%")
    
    # Test all conditions (exact same logic as websocket.py)
    bb_condition = bb_value <= 0.30
    ema_condition = ema_ratio > 0.95
    drop_condition = drop_confirmed
    
    print(f"\n🎯 BUY CONDITIONS CHECK:")
    print(f"   1. BB ≤ 0.30: {'✅' if bb_condition else '❌'} ({bb_value:.3f})")
    print(f"   2. EMA > 0.95: {'✅' if ema_condition else '❌'} ({ema_ratio:.4f})")
    print(f"   3. Drop ≥ 2%: {'✅' if drop_condition else '❌'} ({drop_pct:.2f}%)")
    
    all_met = bb_condition and ema_condition and drop_condition
    
    print(f"\n{'🎉 BUY SIGNAL TRIGGERED!' if all_met else '❌ CONDITIONS NOT MET'}")
    
    if all_met:
        print(f"🚀 Perfect! Bot would buy {price:.6f} DOGEFDUSD")
        print(f"   Grid strategy would start with ATR={atr_now:.6f}")
    else:
        missing = []
        if not bb_condition:
            missing.append(f"BB too high ({bb_value:.3f})")
        if not ema_condition:
            missing.append(f"Too far from EMA ({ema_ratio:.4f})")
        if not drop_condition:
            missing.append(f"No 2% drop ({drop_pct:.2f}%)")
        print(f"   Missing: {', '.join(missing)}")
    
    return all_met

def test_websocket_import():
    """Test that the websocket module imports correctly"""
    print("\n🔌 Testing WebSocket Import...")
    
    try:
        from bot.services.websocket import handle_kline, start_websocket, strategy
        print("✅ WebSocket module imported successfully")
        
        # Check if strategy object is properly initialized
        print(f"✅ Strategy object: {type(strategy).__name__}")
        print(f"✅ Strategy realised PnL: {strategy.realised}")
        print(f"✅ Strategy cycle: {strategy.cycle}")
        
        return True
    except Exception as e:
        print(f"❌ WebSocket import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE BUY CONDITION TEST\n")
    
    # Test 1: Perfect buy scenario
    buy_triggered = create_perfect_buy_scenario()
    
    # Test 2: WebSocket import
    import_ok = test_websocket_import()
    
    print(f"\n🏁 FINAL RESULTS:")
    print(f"   Perfect scenario test: {'🎯 PASS' if buy_triggered else '⏳ NEEDS TUNING'}")
    print(f"   WebSocket import: {'✅ PASS' if import_ok else '❌ FAIL'}")
    
    if buy_triggered and import_ok:
        print(f"\n🎉 ALL TESTS PASSED! DogeBot buy conditions are working perfectly!")
        print(f"🚀 Bot is ready for live DOGE trading on Railway!")
    else:
        print(f"\n⚠️ Some tests need attention before live trading.")
