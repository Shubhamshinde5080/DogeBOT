#!/usr/bin/env python3
"""
DogeBot Manual Testing Script
Test buy/sell functionality with controlled conditions
"""

import sys
import os
sys.path.append('/app')

from bot.core.order_mgr import OrderMgr
from bot.core.strategy import GridStrategy
from bot.utils.account_monitor import AccountMonitor
import argparse

def test_simple_buy_order(order_mgr, price=None, qty=10):
    """Test a simple buy order"""
    if not price:
        # Get current market price and place order slightly below
        monitor = AccountMonitor()
        current_price = monitor.get_current_price("DOGEFDUSD")
        if current_price:
            price = current_price * 0.999  # 0.1% below market
        else:
            print("❌ Could not get current price")
            return
    
    print(f"🔨 Testing BUY order: {qty} DOGEFDUSD @ ${price:.6f}")
    try:
        result = order_mgr.post_limit_maker("BUY", price, qty)
        print(f"✅ Buy order result: {result}")
        return result
    except Exception as e:
        print(f"❌ Buy order failed: {e}")
        return None

def test_simple_sell_order(order_mgr, price=None, qty=10):
    """Test a simple sell order"""
    if not price:
        # Get current market price and place order slightly above
        monitor = AccountMonitor()
        current_price = monitor.get_current_price("DOGEFDUSD")
        if current_price:
            price = current_price * 1.001  # 0.1% above market
        else:
            print("❌ Could not get current price")
            return
    
    print(f"🔨 Testing SELL order: {qty} DOGEFDUSD @ ${price:.6f}")
    try:
        result = order_mgr.post_limit_maker("SELL", price, qty)
        print(f"✅ Sell order result: {result}")
        return result
    except Exception as e:
        print(f"❌ Sell order failed: {e}")
        return None

def test_strategy_conditions():
    """Test strategy entry conditions manually"""
    print("🧪 Testing Strategy Conditions")
    
    # Create test strategy
    order_mgr = OrderMgr(symbol="DOGEFDUSD")
    strategy = GridStrategy(order_mgr=order_mgr)
    
    # Get current price for testing
    monitor = AccountMonitor()
    current_price = monitor.get_current_price("DOGEFDUSD")
    
    if not current_price:
        print("❌ Cannot get current price")
        return
    
    print(f"📊 Current DOGEFDUSD price: ${current_price:.6f}")
    
    # Test ATR calculation with dummy data
    test_atr = current_price * 0.02  # 2% ATR for testing
    
    print(f"🔧 Test Parameters:")
    print(f"  - Entry Price: ${current_price:.6f}")
    print(f"  - Test ATR: ${test_atr:.6f}")
    print(f"  - Step Size: ${strategy.step_mult * test_atr:.6f}")
    print(f"  - Initial Qty: {strategy.qty0}")
    print(f"  - Qty Increment: {strategy.qty_inc}")
    
    # Force start a cycle for testing
    print("\n🚀 Force starting test cycle...")
    strategy.start_cycle(current_price, test_atr)
    
    print(f"✅ Cycle started!")
    print(f"  - Next buy price: ${strategy.next_buy:.6f}")
    print(f"  - Next quantity: {strategy.qty_next}")
    print(f"  - Step size: ${strategy.step:.6f}")
    
    return strategy

def test_market_buy_sell():
    """Test immediate market-like orders"""
    print("🏪 Testing Market-like Orders")
    
    order_mgr = OrderMgr(symbol="DOGEFDUSD")
    monitor = AccountMonitor()
    
    current_price = monitor.get_current_price("DOGEFDUSD")
    if not current_price:
        print("❌ Cannot get current price")
        return
    
    print(f"📊 Current market price: ${current_price:.6f}")
    
    # Test aggressive buy (close to market price)
    buy_price = current_price * 0.9999  # Very close to market
    print(f"\n🔨 Testing aggressive BUY @ ${buy_price:.6f}")
    
    try:
        buy_result = order_mgr.post_limit_maker("BUY", buy_price, 5)
        if buy_result:
            print("✅ Aggressive buy order placed")
    except Exception as e:
        print(f"❌ Aggressive buy failed: {e}")
    
    # Test aggressive sell (close to market price)
    sell_price = current_price * 1.0001  # Very close to market
    print(f"\n🔨 Testing aggressive SELL @ ${sell_price:.6f}")
    
    try:
        sell_result = order_mgr.post_limit_maker("SELL", sell_price, 5)
        if sell_result:
            print("✅ Aggressive sell order placed")
    except Exception as e:
        print(f"❌ Aggressive sell failed: {e}")

def main():
    parser = argparse.ArgumentParser(description='DogeBot Manual Testing')
    parser.add_argument('--test', choices=['buy', 'sell', 'strategy', 'market', 'all'], 
                       default='all', help='Test type to run')
    parser.add_argument('--price', type=float, help='Custom price for orders')
    parser.add_argument('--qty', type=float, default=10, help='Quantity for test orders')
    
    args = parser.parse_args()
    
    print("🤖 DogeBot Manual Testing Suite")
    print("=" * 50)
    
    # Initialize components
    order_mgr = OrderMgr(symbol="DOGEFDUSD")
    
    if args.test in ['buy', 'all']:
        print("\n📥 Testing BUY Orders:")
        test_simple_buy_order(order_mgr, args.price, args.qty)
    
    if args.test in ['sell', 'all']:
        print("\n📤 Testing SELL Orders:")
        test_simple_sell_order(order_mgr, args.price, args.qty)
    
    if args.test in ['strategy', 'all']:
        print("\n🎯 Testing Strategy Logic:")
        test_strategy_conditions()
    
    if args.test in ['market', 'all']:
        print("\n🏪 Testing Market-like Orders:")
        test_market_buy_sell()
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    main()
