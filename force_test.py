#!/usr/bin/env python3
"""
Force Trading Test - Immediately trigger bot trading for testing
"""

import sys
import os
sys.path.append('/home/shubham/DogeBot')

from bot.services.websocket import strategy, bars
from bot.utils.account_monitor import AccountMonitor
import pandas as pd
import numpy as np

def force_strategy_start():
    """Force start the strategy with current market conditions"""
    print("🚀 Force Starting Strategy for Testing")
    
    # Get current market price
    monitor = AccountMonitor()
    current_price = monitor.get_current_price("DOGEFDUSD")
    
    if not current_price:
        print("❌ Cannot get current price")
        return False
    
    print(f"📊 Current DOGEFDUSD price: ${current_price:.6f}")
    
    # Create fake ATR for testing (2% of price)
    test_atr = current_price * 0.02
    
    print(f"🔧 Using test ATR: ${test_atr:.6f} (2% of price)")
    
    # Force start the cycle
    strategy.start_cycle(current_price, test_atr)
    
    print("✅ Strategy cycle force-started!")
    print(f"  - Cycle active: {strategy.cycle}")
    print(f"  - Next buy price: ${strategy.next_buy:.6f}")
    print(f"  - Next quantity: {strategy.qty_next}")
    print(f"  - Step size: ${strategy.step:.6f}")
    print(f"  - Available funds: ${strategy.funds_free():.2f}")
    
    return True

def create_test_candles():
    """Create some test candle data to satisfy the 10-candle requirement"""
    print("📊 Creating test candle data...")
    
    monitor = AccountMonitor()
    current_price = monitor.get_current_price("DOGEFDUSD")
    
    if not current_price:
        print("❌ Cannot get current price")
        return False
    
    # Create 15 test candles with realistic price movement
    dates = pd.date_range(end=pd.Timestamp.now(), periods=15, freq='15T')
    
    # Generate realistic OHLC data around current price
    base_price = current_price
    price_variation = base_price * 0.02  # 2% variation
    
    test_data = []
    for i, date in enumerate(dates):
        # Random walk with slight downward bias for testing
        if i == 0:
            open_price = base_price
        else:
            open_price = test_data[i-1]['close']
        
        # Add some random movement
        movement = np.random.normal(-0.001, 0.01)  # Slight downward bias
        close_price = open_price * (1 + movement)
        
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.005)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.005)))
        
        test_data.append({
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price
        })
    
    # Update the global bars DataFrame
    global bars
    for i, (date, data) in enumerate(zip(dates, test_data)):
        bars.loc[date] = [data['open'], data['high'], data['low'], data['close']]
    
    print(f"✅ Created {len(bars)} test candles")
    print(f"  - Price range: ${bars['low'].min():.6f} - ${bars['high'].max():.6f}")
    print(f"  - Latest close: ${bars['close'].iloc[-1]:.6f}")
    
    return True

def trigger_test_trade():
    """Trigger a test trade by simulating price drop"""
    if not strategy.cycle:
        print("❌ Strategy cycle not active. Run force_strategy_start() first.")
        return False
    
    print(f"🎯 Triggering test trade...")
    print(f"  - Next buy trigger: ${strategy.next_buy:.6f}")
    print(f"  - Available funds: ${strategy.funds_free():.2f}")
    
    # Simulate price hitting the buy level
    test_price = strategy.next_buy + 0.000001  # Just above trigger
    test_atr = strategy.step / strategy.step_mult  # Recreate ATR from step
    
    print(f"🔄 Simulating price at ${test_price:.6f}")
    
    # Call the strategy's on_tick method
    strategy.on_tick(test_price, test_atr)
    
    print(f"✅ Trade simulation complete")
    print(f"  - Open ladders: {len(strategy.ladders)}")
    print(f"  - Next buy level: ${strategy.next_buy:.6f}")
    print(f"  - Next quantity: {strategy.qty_next}")
    
    return True

def main():
    print("🤖 DogeBot Force Trading Test")
    print("=" * 50)
    
    print("\n1️⃣ Creating test candle data...")
    if not create_test_candles():
        return
    
    print("\n2️⃣ Force starting strategy...")
    if not force_strategy_start():
        return
    
    print("\n3️⃣ Triggering test trade...")
    trigger_test_trade()
    
    print("\n✅ Force trading test complete!")
    print("\n📊 Final Status:")
    print(f"  - Strategy active: {strategy.cycle}")
    print(f"  - Realized PnL: ${strategy.realised:.2f}")
    print(f"  - Open positions: {len(strategy.ladders)}")
    print(f"  - Available funds: ${strategy.funds_free():.2f}")

if __name__ == "__main__":
    main()
