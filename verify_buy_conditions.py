#!/usr/bin/env python3
"""
Real-time Buy Condition Verification
Tests current market conditions against DogeBot buy requirements
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add bot path
sys.path.append('/home/shubham/DogeBot')

from bot.core.indicators import atr, ema, boll_pct

def simulate_current_conditions():
    """Simulate current market conditions to test buy logic"""
    
    print("🔍 DOGEBOT BUY CONDITIONS VERIFICATION")
    print("=" * 60)
    
    # Simulate recent DOGEFDUSD price data based on your logs
    # Candles #5-14 from your Railway logs
    price_data = [
        0.21373000,  # Candle #5
        0.21448000,  # Candle #6  
        0.21141000,  # Candle #7
        0.21230000,  # Candle #8
        0.21398000,  # Candle #9
        0.21422000,  # Candle #10
        0.21338000,  # Candle #11
        0.21145000,  # Candle #12
        0.21149000,  # Candle #13
        0.21188000,  # Candle #14 (latest)
    ]
    
    # Create mock OHLC data (simplified for testing)
    df = pd.DataFrame({
        'open': price_data,
        'high': [p * 1.002 for p in price_data],  # +0.2% high
        'low': [p * 0.998 for p in price_data],   # -0.2% low  
        'close': price_data,
        'volume': [1000000] * len(price_data)  # Mock volume
    })
    
    print(f"📊 MARKET DATA ANALYSIS:")
    print(f"   Latest Price: {df['close'].iloc[-1]:.6f} FDUSD")
    print(f"   Price Range: {df['close'].min():.6f} - {df['close'].max():.6f}")
    print(f"   Candles Available: {len(df)}")
    
    # Calculate technical indicators
    df['atr'] = atr(df, win=min(14, len(df)))
    df['ema'] = ema(df['close'], span=min(200, len(df)))
    df['bb'] = boll_pct(df, win=min(20, len(df)))
    
    # Get latest values
    latest_price = df['close'].iloc[-1]
    latest_atr = df['atr'].iloc[-1]
    latest_bb = df['bb'].iloc[-1]
    latest_ema = df['ema'].iloc[-1]
    
    print(f"\n🧮 TECHNICAL INDICATORS:")
    print(f"   ATR (14): {latest_atr:.6f}")
    print(f"   EMA (200): {latest_ema:.6f}")
    print(f"   BB %: {latest_bb:.3f}")
    print(f"   EMA Ratio: {latest_price/latest_ema:.4f}")
    
    # Check each condition
    print(f"\n🎯 BUY CONDITIONS CHECK:")
    
    # 1. Data requirement
    data_ok = len(df) >= 10
    print(f"   1. ✅ Data Collection: {len(df)}/10 candles {'✅ PASS' if data_ok else '❌ FAIL'}")
    
    # 2. ATR validity
    atr_ok = not pd.isna(latest_atr)
    print(f"   2. {'✅' if atr_ok else '❌'} ATR Valid: {latest_atr:.6f} {'✅ PASS' if atr_ok else '❌ FAIL'}")
    
    # 3. Bollinger Band condition
    bb_condition = latest_bb <= 0.30
    print(f"   3. {'✅' if bb_condition else '❌'} Bollinger Band: {latest_bb:.3f} <= 0.30 {'✅ PASS' if bb_condition else '❌ FAIL'}")
    
    # 4. EMA condition  
    ema_ratio = latest_price / latest_ema
    ema_condition = ema_ratio > 0.95
    print(f"   4. {'✅' if ema_condition else '❌'} EMA Trend: {ema_ratio:.4f} > 0.95 {'✅ PASS' if ema_condition else '❌ FAIL'}")
    
    # 5. No active cycle (assume true for new deployment)
    cycle_ok = True
    print(f"   5. ✅ No Active Cycle: {'✅ PASS' if cycle_ok else '❌ FAIL'}")
    
    # Overall assessment
    all_conditions = data_ok and atr_ok and bb_condition and ema_condition and cycle_ok
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if all_conditions:
        print(f"   🟢 ALL CONDITIONS MET - BOT WOULD START TRADING!")
        print(f"   🚀 Entry would trigger at next candle close")
    else:
        print(f"   🟡 WAITING FOR CONDITIONS:")
        if not bb_condition:
            print(f"      • BB needs to be <= 0.30 (currently {latest_bb:.3f})")
        if not ema_condition:
            print(f"      • Price needs to be > 95% EMA (currently {ema_ratio:.1%})")
    
    # Grid setup preview
    if all_conditions:
        step_size = 0.25 * latest_atr
        print(f"\n📊 GRID TRADING SETUP:")
        print(f"   Entry Price: {latest_price:.6f}")
        print(f"   Step Size: {step_size:.6f} (25% of ATR)")
        print(f"   First Buy: {latest_price - step_size:.6f}")
        print(f"   Initial Qty: 300 DOGE")
        print(f"   Sell Target: {latest_price + step_size:.6f}")
    
    print(f"\n⏰ NEXT CHECK: Wait for next 15-minute candle close")
    print(f"📈 MARKET STATUS: {'Ready to trade!' if all_conditions else 'Monitoring conditions...'}")

if __name__ == "__main__":
    simulate_current_conditions()
