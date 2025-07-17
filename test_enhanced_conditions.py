#!/usr/bin/env python3
"""
Enhanced Buy Conditions Test
Tests the updated logic with the missing 2% drop condition
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add bot path
sys.path.append('/home/shubham/DogeBot')

from bot.core.indicators import atr, ema, boll_pct

def test_enhanced_conditions():
    """Test the enhanced buy conditions with 2% drop requirement"""
    
    print("🔍 ENHANCED BUY CONDITIONS TEST")
    print("=" * 60)
    
    # Simulate price data with different scenarios
    scenarios = {
        "Scenario A - No Drop": [
            0.21000, 0.21050, 0.21080, 0.21100, 0.21120,  # Rising prices
            0.21140, 0.21160, 0.21180, 0.21200, 0.21188   # Latest: slight dip
        ],
        "Scenario B - 2% Drop": [
            0.21500, 0.21480, 0.21450, 0.21400, 0.21350,  # Initial decline
            0.21300, 0.21250, 0.21200, 0.21180, 0.21074   # 2% drop from high
        ],
        "Scenario C - 3% Drop": [
            0.22000, 0.21950, 0.21900, 0.21800, 0.21700,  # Stronger decline
            0.21600, 0.21500, 0.21400, 0.21350, 0.21340   # 3% drop from high
        ]
    }
    
    for scenario_name, prices in scenarios.items():
        print(f"\n📊 {scenario_name}")
        print("-" * 40)
        
        # Create OHLC data
        df = pd.DataFrame({
            'open': prices,
            'high': [p * 1.002 for p in prices],
            'low': [p * 0.998 for p in prices],
            'close': prices,
            'volume': [1000000] * len(prices)
        })
        
        # Calculate indicators
        df['atr'] = atr(df, win=min(14, len(df)))
        df['ema'] = ema(df['close'], span=min(200, len(df)))
        df['bb'] = boll_pct(df, win=min(20, len(df)))
        
        # Get latest values
        latest_price = df['close'].iloc[-1]
        latest_atr = df['atr'].iloc[-1]
        latest_bb = df['bb'].iloc[-1]
        latest_ema = df['ema'].iloc[-1]
        
        # Check 2% drop condition
        def check_recent_drop(df_data, lookback=2):
            if len(df_data) < lookback + 1:
                return False
            recent_high = df_data['high'].tail(lookback).max()
            current_price = df_data['close'].iloc[-1]
            drop_percent = (recent_high - current_price) / recent_high
            return drop_percent >= 0.02
        
        drop_confirmed = check_recent_drop(df)
        
        # Calculate drop percentage for display
        recent_high = df['high'].tail(2).max()
        drop_percent = (recent_high - latest_price) / recent_high * 100
        
        print(f"   Price: {latest_price:.5f}")
        print(f"   Recent High: {recent_high:.5f}")
        print(f"   Drop: {drop_percent:.1f}%")
        
        # Check all conditions
        data_ok = len(df) >= 10
        atr_ok = not pd.isna(latest_atr)
        bb_condition = latest_bb <= 0.30
        ema_condition = latest_price > 0.95 * latest_ema
        
        print(f"\n   Conditions:")
        print(f"   ✅ Data: {len(df)}/10")
        print(f"   {'✅' if atr_ok else '❌'} ATR: {latest_atr:.6f}")
        print(f"   {'✅' if bb_condition else '❌'} BB: {latest_bb:.3f} ≤ 0.30")
        print(f"   {'✅' if ema_condition else '❌'} EMA: {latest_price/latest_ema:.4f} > 0.95")
        print(f"   {'✅' if drop_confirmed else '❌'} 2% Drop: {drop_confirmed}")
        
        # Overall result
        all_met = data_ok and atr_ok and bb_condition and ema_condition and drop_confirmed
        print(f"\n   Result: {'🎯 TRADE TRIGGERED!' if all_met else '⏳ Waiting...'}")
        
        if drop_confirmed:
            step_size = 0.25 * latest_atr if not pd.isna(latest_atr) else 0.0005
            print(f"   Grid Preview: Entry={latest_price:.5f}, Step={step_size:.5f}")

if __name__ == "__main__":
    test_enhanced_conditions()
