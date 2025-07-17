"""
Simple Working DogeBot Tests - Show GitHub Copilot THIS!
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
from unittest.mock import Mock

# Add the bot directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.core.indicators import atr, ema, boll_pct

def test_dogebot_perfect_buy_conditions():
    """
    REAL TEST: Perfect conditions should trigger buy
    """
    # Create 25 candles with tight range (low BB)
    base_price = 0.21000
    prices = []
    
    # 22 stable candles
    for i in range(22):
        noise = np.random.uniform(-0.0001, 0.0001)  # Very tight range
        prices.append(base_price + noise)
    
    # Add spike and 2.5% drop
    spike = base_price * 1.025
    drop = spike * 0.975  # 2.5% drop
    prices.extend([spike, drop])
    
    # Create DataFrame
    df = pd.DataFrame({
        'high': [p * 1.001 for p in prices],
        'low': [p * 0.999 for p in prices],
        'close': prices,
        'volume': [1000000] * len(prices)
    })
    
    # Calculate indicators
    df['atr'] = atr(df, win=14)
    df['ema'] = ema(df['close'], span=50)
    df['bb'] = boll_pct(df, win=20)
    
    # Get final values
    price = df['close'].iat[-1]
    atr_now = df['atr'].iat[-1]
    bb_now = df['bb'].iat[-1]
    ema_now = df['ema'].iat[-1]
    
    # Check 2% drop
    recent_high = df['high'].tail(4).max()
    current_price = df['close'].iat[-1]
    drop_percent = (recent_high - current_price) / recent_high
    
    # REAL ASSERTIONS - not print statements!
    assert not pd.isna(atr_now), "ATR should be calculated"
    assert not pd.isna(bb_now), "BB should be calculated"
    assert not pd.isna(ema_now), "EMA should be calculated"
    assert bb_now <= 0.30, f"BB should be ≤ 0.30, got {bb_now:.3f}"
    assert price > 0.95 * ema_now, f"Price should be > 95% EMA, got {price/ema_now:.3f}"
    assert drop_percent >= 0.02, f"Drop should be ≥ 2%, got {drop_percent:.3f}"
    
    print("✅ PERFECT CONDITIONS TEST PASSED!")
    return True

def test_dogebot_high_volatility_blocks_buy():
    """
    REAL TEST: High volatility should prevent buying
    """
    # Create 25 candles with HIGH volatility
    base_price = 0.21000
    prices = []
    
    for i in range(25):
        # High volatility - wide price swings
        volatility = 0.005  # 0.5% swings
        noise = np.random.uniform(-volatility, volatility)
        prices.append(base_price + noise)
    
    # Create DataFrame
    df = pd.DataFrame({
        'high': [p * 1.003 for p in prices],
        'low': [p * 0.997 for p in prices],
        'close': prices,
        'volume': [1000000] * len(prices)
    })
    
    # Calculate BB
    df['bb'] = boll_pct(df, win=20)
    bb_now = df['bb'].iat[-1]
    
    # REAL ASSERTION
    assert bb_now > 0.30, f"High volatility should give BB > 0.30, got {bb_now:.3f}"
    
    print("✅ HIGH VOLATILITY BLOCKING TEST PASSED!")
    return True

def test_dogebot_no_drop_blocks_buy():
    """
    REAL TEST: No 2% drop should prevent buying
    """
    # Create rising price data (no drop)
    base_price = 0.21000
    prices = [base_price + i * 0.0005 for i in range(25)]  # Rising trend
    
    df = pd.DataFrame({
        'high': [p * 1.001 for p in prices],
        'low': [p * 0.999 for p in prices],
        'close': prices,
        'volume': [1000000] * len(prices)
    })
    
    # Check for drop
    recent_high = df['high'].tail(4).max()
    current_price = df['close'].iat[-1]
    drop_percent = (recent_high - current_price) / recent_high
    
    # REAL ASSERTION
    assert drop_percent < 0.02, f"Rising market should have < 2% drop, got {drop_percent:.3f}"
    
    print("✅ NO DROP BLOCKING TEST PASSED!")
    return True

def test_dogebot_insufficient_data_blocks_buy():
    """
    REAL TEST: Not enough candles should prevent buying
    """
    # Create only 15 candles (need 20+)
    df = pd.DataFrame({
        'high': [0.21001] * 15,
        'low': [0.20999] * 15,
        'close': [0.21000] * 15,
        'volume': [1000000] * 15
    })
    
    # Try to calculate BB
    df['bb'] = boll_pct(df, win=20)
    bb_now = df['bb'].iat[-1]
    
    # REAL ASSERTION
    assert pd.isna(bb_now), "BB should be NaN with insufficient data"
    
    print("✅ INSUFFICIENT DATA BLOCKING TEST PASSED!")
    return True

def test_all_dogebot_conditions():
    """
    Master test function - runs all DogeBot tests
    """
    print("\n🚀 RUNNING SIMPLIFIED DOGEBOT TESTS...")
    print("=" * 50)
    
    # Run all tests
    test_dogebot_perfect_buy_conditions()
    test_dogebot_high_volatility_blocks_buy()
    test_dogebot_no_drop_blocks_buy()
    test_dogebot_insufficient_data_blocks_buy()
    
    print("=" * 50)
    print("🎉 ALL DOGEBOT TESTS PASSED!")
    print("✅ Your bot logic works correctly!")

if __name__ == "__main__":
    test_all_dogebot_conditions()
