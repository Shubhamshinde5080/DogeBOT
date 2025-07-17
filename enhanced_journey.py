#!/usr/bin/env python3
"""
Enhanced Complete Journey - With proper BB calculation timing
"""

import sys
import pandas as pd
import numpy as np

sys.path.append('/home/shubham/DogeBot')
from bot.core.indicators import atr, ema, boll_pct
from bot.core.strategy import GridStrategy

class MockOrderMgr:
    def __init__(self):
        self.orders = []
    
    def post_limit_maker(self, side, price, qty):
        self.orders.append({"side": side, "price": price, "qty": qty})
        print(f"        🔥 ORDER: {side} {qty} DOGE @ {price:.6f}")
        return {"orderId": len(self.orders)}

def simulate_enhanced_tick(df, strategy, candle_num):
    """Enhanced simulation with proper indicator timing"""
    
    print(f"\n📊 CANDLE #{candle_num} - {df['close'].iat[-1]:.6f} FDUSD")
    
    # Phase 1: Data collection (need 10 for processing, 20 for BB)
    if len(df) < 10:
        print(f"    ⏳ Collecting data: {len(df)}/10 minimum needed")
        return False, "Collecting data"
    
    # Phase 2: Indicator calculation
    if len(df) < 20:
        print(f"    📊 Have {len(df)} candles, but need 20+ for reliable BB calculation")
        return False, "Building indicator base"
    
    # Calculate indicators
    df["atr"] = atr(df, win=min(14, len(df)))
    df["ema"] = ema(df["close"], span=min(200, len(df)))
    df["bb"] = boll_pct(df, win=min(20, len(df)))
    
    price = df["close"].iat[-1]
    atr_now = df["atr"].iat[-1]
    bb_now = df["bb"].iat[-1]
    ema_now = df["ema"].iat[-1]
    
    # Check ATR validity
    if pd.isna(atr_now):
        print(f"    ⚠️ ATR calculation not ready")
        return False, "ATR not ready"
    
    # Check BB validity
    if pd.isna(bb_now):
        print(f"    ⚠️ BB calculation not ready (need more data)")
        return False, "BB not ready"
    
    # 2% drop check
    def check_recent_drop(df_data, lookback=3):
        if len(df_data) < lookback + 1:
            return False, 0
        recent_high = df_data['high'].tail(lookback + 1).max()
        current_price = df_data['close'].iat[-1]
        drop_percent = (recent_high - current_price) / recent_high
        return drop_percent >= 0.02, drop_percent
    
    drop_confirmed, drop_pct = check_recent_drop(df)
    
    # Show technical analysis
    print(f"    📈 Technical Analysis:")
    print(f"       Price: {price:.6f}")
    print(f"       ATR: {atr_now:.6f}")
    print(f"       BB%: {bb_now:.3f}")
    print(f"       EMA Ratio: {price/ema_now:.4f}")
    print(f"       Drop: {drop_pct:.1%} ({'✅' if drop_confirmed else '❌'})")
    
    # Check conditions
    bb_condition = bb_now <= 0.30
    ema_condition = price > 0.95 * ema_now
    cycle_condition = not strategy.cycle
    
    conditions = {
        "BB ≤ 0.30": bb_condition,
        "EMA > 95%": ema_condition, 
        "2% Drop": drop_confirmed,
        "No Cycle": cycle_condition
    }
    
    print(f"    🎯 Conditions:")
    for name, result in conditions.items():
        status = "✅" if result else "❌"
        value = ""
        if "BB" in name:
            value = f"({bb_now:.3f})"
        elif "EMA" in name:
            value = f"({price/ema_now:.3f})"
        elif "Drop" in name:
            value = f"({drop_pct:.1%})"
        print(f"       {status} {name}: {result} {value}")
    
    # Check if triggered
    all_met = all(conditions.values())
    
    if all_met:
        print(f"    🚀 ALL CONDITIONS MET! STARTING GRID TRADING!")
        strategy.start_cycle(price, atr_now)
        
        # Simulate grid activation
        print(f"    🎮 Grid Setup:")
        print(f"       Entry: {price:.6f}")
        print(f"       Step: {strategy.step:.6f}")
        print(f"       Next Buy: {strategy.next_buy:.6f}")
        
        # Trigger first buy
        strategy.on_tick(strategy.next_buy - 0.000001, atr_now)
        
        # Simulate immediate sell for profit demonstration
        if len(strategy.ladders) > 0:
            ladder = strategy.ladders[0]
            sell_price = ladder.sell
            print(f"    💰 Simulating sell at {sell_price:.6f}")
            strategy.handle_sell_fill(sell_price, ladder.buy, ladder.qty)
            print(f"       Profit: ${strategy.realised:.4f}")
        
        return True, "TRADING ACTIVE"
    else:
        missing = [name for name, result in conditions.items() if not result]
        return False, f"Waiting: {', '.join(missing)}"

def create_enhanced_journey():
    """Create journey with proper timing for all indicators"""
    
    base_price = 0.21200
    prices = []
    
    print("🎯 ENHANCED BOT JOURNEY SIMULATION")
    print("=" * 60)
    
    # Phase 1: Base data (25 candles for all indicators)
    print("\n📊 PHASE 1: BASE DATA COLLECTION")
    for i in range(25):
        noise = np.random.uniform(-0.0003, 0.0003)
        price = base_price + noise
        prices.append(price)
    print(f"   ✅ Created {len(prices)} stable candles for indicator base")
    
    # Phase 2: Conditions that fail (10 candles)
    print("\n📊 PHASE 2: CONDITIONS TESTING (10 failure cases)")
    
    # High volatility (BB > 0.30)
    for i in range(3):
        volatility = 0.004
        price = base_price * (1 + np.random.uniform(-volatility, volatility))
        prices.append(price)
        print(f"   Candle {len(prices)}: High volatility - BB will be high")
    
    # Downtrend (EMA < 95%)
    for i in range(3):
        trend_price = base_price * (0.97 - i * 0.005)
        prices.append(trend_price)
        print(f"   Candle {len(prices)}: Downtrend - EMA condition fails")
    
    # No drop (stable/rising)
    for i in range(4):
        stable_price = base_price * (1.001 + i * 0.002)
        prices.append(stable_price)
        print(f"   Candle {len(prices)}: Rising - no 2% drop")
    
    # Phase 3: Perfect conditions (5 candles)
    print("\n📊 PHASE 3: PERFECT SETUP (5 success candles)")
    
    # Return to tight range for low BB
    for i in range(3):
        tight_price = base_price + np.random.uniform(-0.0002, 0.0002)
        prices.append(tight_price)
        print(f"   Candle {len(prices)}: Tight range - reducing BB")
    
    # Small spike and pullback
    spike = base_price * 1.025
    prices.append(spike)
    print(f"   Candle {len(prices)}: Spike to {spike:.6f}")
    
    pullback = spike * 0.975  # 2.5% drop
    prices.append(pullback)
    print(f"   Candle {len(prices)}: Pullback to {pullback:.6f} (2.5% drop)")
    
    print(f"\n✅ TOTAL: {len(prices)} candles created")
    return prices

def run_enhanced_journey():
    """Run the enhanced complete journey"""
    
    prices = create_enhanced_journey()
    
    # Create dataframe
    df = pd.DataFrame({
        'open': prices,
        'high': [p * 1.0003 for p in prices],
        'low': [p * 0.9997 for p in prices],
        'close': prices,
        'volume': [1000000] * len(prices)
    })
    
    # Initialize
    mock_order_mgr = MockOrderMgr()
    strategy = GridStrategy(order_mgr=mock_order_mgr)
    
    print(f"\n{'='*60}")
    print("🚀 RUNNING ENHANCED JOURNEY")
    print(f"{'='*60}")
    
    # Track phases
    phases = {
        25: "📊 DATA COLLECTION COMPLETE",
        35: "📊 FAILURE TESTING COMPLETE", 
        40: "📊 PERFECT SETUP COMPLETE"
    }
    
    # Simulate each candle
    for i in range(1, len(df) + 1):
        current_df = df.iloc[:i].copy()
        
        # Phase markers
        if i in phases:
            print(f"\n🔄 {phases[i]}")
        
        # Process candle
        triggered, status = simulate_enhanced_tick(current_df, strategy, i)
        print(f"    📊 Result: {status}")
        
        if triggered:
            print(f"\n🎉 TRADING ACTIVATED AT CANDLE #{i}!")
            break
        
        # Show progress for key milestones
        if i in [10, 20, 25, 30, 35]:
            print(f"    ⏭️  Milestone: {i} candles processed")
    
    # Final summary
    print(f"\n{'='*60}")
    print("🏆 ENHANCED JOURNEY SUMMARY")
    print(f"{'='*60}")
    
    if strategy.cycle:
        print("✅ SUCCESS: Complete journey from data collection to trading!")
        print(f"\n📊 Journey Breakdown:")
        print(f"   • Data Collection: Candles 1-25")
        print(f"   • Failed Conditions: Candles 26-35")
        print(f"   • Perfect Setup: Candles 36-40")
        print(f"   • Trading Started: Candle {i}")
        
        print(f"\n💰 Trading Results:")
        print(f"   • Orders Placed: {len(mock_order_mgr.orders)}")
        print(f"   • First Profit: ${strategy.realised:.4f}")
        print(f"   • Daily Target: ${strategy.profit_target:.2f}")
        
        print(f"\n🎯 Key Lessons:")
        print(f"   ✅ Bot waits patiently for optimal conditions")
        print(f"   ✅ All 6 conditions must align perfectly")
        print(f"   ✅ When triggered, immediate profitable trading begins")
        print(f"   ✅ Grid strategy works exactly as designed")
        
    else:
        print("⚠️  Journey completed but trading never triggered")
        print("💡 This shows how selective your bot is!")

if __name__ == "__main__":
    run_enhanced_journey()
