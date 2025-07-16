#!/usr/bin/env python3
"""
DogeBot Comprehensive Test Suite
Tests all components to ensure everything is working properly
"""

import sys
import os
import time
import traceback
sys.path.append('/home/shubham/DogeBot')

from bot.utils.account_monitor import AccountMonitor
from bot.core.order_mgr import OrderMgr
from bot.services.websocket import strategy

def test_header(test_name):
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def test_result(success, message):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")
    return success

def test_1_environment_variables():
    """Test environment variables and configuration"""
    test_header("Environment Variables & Configuration")
    
    success = True
    
    # Check .env file exists
    env_exists = os.path.exists('.env')
    success &= test_result(env_exists, f".env file exists: {env_exists}")
    
    # Check required environment variables
    required_vars = ['API_KEY', 'API_SECRET', 'BASE_URL']
    for var in required_vars:
        value = os.getenv(var)
        exists = value is not None and len(value) > 0
        success &= test_result(exists, f"{var} is set: {exists}")
    
    return success

def test_2_account_connectivity():
    """Test Binance API connectivity and account access"""
    test_header("Binance API Connectivity")
    
    success = True
    
    try:
        monitor = AccountMonitor()
        
        # Test price fetching
        price = monitor.get_current_price("DOGEFDUSD")
        price_success = price is not None and price > 0
        success &= test_result(price_success, f"DOGEFDUSD price fetch: ${price:.6f}" if price_success else "Price fetch failed")
        
        # Test account balance
        balances = monitor.get_account_balance()
        balance_success = isinstance(balances, dict) and len(balances) > 0
        success &= test_result(balance_success, f"Account balance fetch: {len(balances) if balance_success else 0} assets")
        
        # Check key balances
        key_assets = ['FDUSD', 'DOGE']
        for asset in key_assets:
            if asset in balances:
                balance = balances[asset]['total']
                has_balance = balance > 0
                success &= test_result(has_balance, f"{asset} balance: {balance:.2f}")
        
    except Exception as e:
        success = False
        test_result(False, f"Account connectivity failed: {str(e)[:100]}")
    
    return success

def test_3_order_manager():
    """Test order management system"""
    test_header("Order Management System")
    
    success = True
    
    try:
        order_mgr = OrderMgr()
        
        # Test order manager initialization
        init_success = order_mgr is not None
        success &= test_result(init_success, "OrderMgr initialization")
        
        # Test small buy order (dry run style - very small amount)
        try:
            # Get current price for realistic order
            monitor = AccountMonitor()
            current_price = monitor.get_current_price("DOGEFDUSD")
            
            if current_price:
                # Place a very small test buy order slightly below market
                test_price = current_price * 0.99  # 1% below current price
                test_qty = 10  # Small test quantity
                
                print(f"  🔸 Testing buy order: {test_qty} DOGEFDUSD @ ${test_price:.6f}")
                
                buy_result = order_mgr.post_limit_maker("BUY", test_price, test_qty)
                buy_success = buy_result is not None and 'orderId' in buy_result
                success &= test_result(buy_success, f"Test buy order: Order ID {buy_result.get('orderId', 'N/A') if buy_success else 'Failed'}")
                
                if buy_success:
                    # Cancel the test order immediately
                    cancel_result = order_mgr.cancel_order(buy_result['orderId'])
                    cancel_success = cancel_result is not None
                    test_result(cancel_success, f"Cancel test order: {'Success' if cancel_success else 'Failed'}")
        
        except Exception as e:
            success = False
            test_result(False, f"Order test failed: {str(e)[:100]}")
    
    except Exception as e:
        success = False
        test_result(False, f"OrderMgr initialization failed: {str(e)[:100]}")
    
    return success

def test_4_strategy_engine():
    """Test strategy engine and grid logic"""
    test_header("Strategy Engine & Grid Logic")
    
    success = True
    
    try:
        # Test strategy initialization
        strategy_init = strategy is not None
        success &= test_result(strategy_init, "Strategy engine initialization")
        
        # Test strategy state
        initial_cycle = strategy.cycle
        success &= test_result(not initial_cycle, f"Initial cycle state: {initial_cycle} (should be False)")
        
        # Test funds calculation
        try:
            free_funds = strategy.funds_free()
            funds_success = free_funds > 0
            success &= test_result(funds_success, f"Available funds: ${free_funds:.2f}")
        except Exception as e:
            success = False
            test_result(False, f"Funds calculation failed: {str(e)[:50]}")
        
        # Test cycle start (simulation)
        try:
            monitor = AccountMonitor()
            current_price = monitor.get_current_price("DOGEFDUSD")
            test_atr = current_price * 0.02  # 2% ATR for testing
            
            if current_price:
                print(f"  🔸 Testing cycle start with price=${current_price:.6f}, ATR=${test_atr:.6f}")
                
                # Save original state
                original_cycle = strategy.cycle
                original_realised = strategy.realised
                original_ladders = len(strategy.ladders)
                
                # Test start cycle
                strategy.start_cycle(current_price, test_atr)
                
                cycle_started = strategy.cycle
                success &= test_result(cycle_started, f"Cycle start: {cycle_started}")
                
                step_set = strategy.step is not None and strategy.step > 0
                success &= test_result(step_set, f"Step size set: ${strategy.step:.6f}" if step_set else "Step not set")
                
                next_buy_set = strategy.next_buy is not None and strategy.next_buy > 0
                success &= test_result(next_buy_set, f"Next buy level: ${strategy.next_buy:.6f}" if next_buy_set else "Next buy not set")
                
                # Reset to original state
                strategy.cycle = original_cycle
                strategy.realised = original_realised
                strategy.ladders.clear()
        
        except Exception as e:
            success = False
            test_result(False, f"Strategy cycle test failed: {str(e)[:100]}")
    
    except Exception as e:
        success = False
        test_result(False, f"Strategy engine test failed: {str(e)[:100]}")
    
    return success

def test_5_docker_container():
    """Test Docker container status"""
    test_header("Docker Container Status")
    
    success = True
    
    try:
        import subprocess
        
        # Check if container is running
        result = subprocess.run(['docker', 'ps', '--filter', 'name=dogebot-container', '--format', '{{.Status}}'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            container_running = 'Up' in result.stdout
            success &= test_result(container_running, f"Container status: {result.stdout.strip()}")
            
            if container_running:
                # Check container logs for activity
                log_result = subprocess.run(['docker', 'logs', 'dogebot-container', '--tail', '5'], 
                                          capture_output=True, text=True)
                
                has_logs = len(log_result.stdout) > 0
                success &= test_result(has_logs, f"Container logs: {'Active' if has_logs else 'No recent activity'}")
                
                # Check for WebSocket connection in logs
                websocket_active = 'WebSocket handshake successful' in log_result.stdout or 'Subscribing to DOGEFDUSD' in log_result.stdout
                success &= test_result(websocket_active, f"WebSocket connection: {'Active' if websocket_active else 'Not detected in recent logs'}")
        else:
            success = False
            test_result(False, "Docker container not found or not running")
    
    except Exception as e:
        success = False
        test_result(False, f"Docker test failed: {str(e)[:100]}")
    
    return success

def test_6_websocket_data():
    """Test WebSocket data reception"""
    test_header("WebSocket Data Reception")
    
    success = True
    
    try:
        import subprocess
        
        # Check recent container logs for data activity
        log_result = subprocess.run(['docker', 'logs', 'dogebot-container', '--tail', '20'], 
                                  capture_output=True, text=True)
        
        if log_result.returncode == 0:
            logs = log_result.stdout
            
            # Check for WebSocket connection
            ws_connected = 'WebSocket handshake successful' in logs
            success &= test_result(ws_connected, f"WebSocket handshake: {'Success' if ws_connected else 'Not found'}")
            
            # Check for data subscription
            data_subscription = 'Subscribing to DOGEFDUSD' in logs
            success &= test_result(data_subscription, f"DOGEFDUSD subscription: {'Active' if data_subscription else 'Not found'}")
            
            # Check for candle data
            candle_data = 'closed kline stored' in logs or 'Closed 15-min candle' in logs
            success &= test_result(candle_data, f"Candle data reception: {'Active' if candle_data else 'Not detected'}")
            
        else:
            success = False
            test_result(False, "Could not retrieve container logs")
    
    except Exception as e:
        success = False
        test_result(False, f"WebSocket test failed: {str(e)[:100]}")
    
    return success

def test_7_trading_readiness():
    """Test overall trading readiness"""
    test_header("Trading Readiness Assessment")
    
    success = True
    
    try:
        monitor = AccountMonitor()
        
        # Check account balances for trading
        balances = monitor.get_account_balance()
        
        trading_assets = {
            'FDUSD': 1000,  # Need at least $1000
            'FDUSD': 1000,  # Need at least $1000  
            'DOGE': 100    # Need at least 100 DOGE
        }
        
        for asset, min_required in trading_assets.items():
            if asset in balances:
                available = balances[asset]['free']
                sufficient = available >= min_required
                success &= test_result(sufficient, f"{asset} ready: {available:.2f} (need {min_required})")
            else:
                success = False
                test_result(False, f"{asset} not found in account")
        
        # Check current market conditions
        current_price = monitor.get_current_price("DOGEFDUSD")
        price_reasonable = 0.15 <= current_price <= 0.35  # Reasonable DOGE price range
        success &= test_result(price_reasonable, f"DOGEFDUSD price: ${current_price:.6f} ({'Reasonable' if price_reasonable else 'Check price'})")
        
        # Check strategy configuration
        config_items = [
            ("Daily target", strategy.profit_target, lambda x: x > 0),
            ("FDUSD cap", strategy.fdusd_cap, lambda x: x >= 1000),
            ("Initial quantity", strategy.qty0, lambda x: x > 0),
            ("Step multiplier", strategy.step_mult, lambda x: 0.1 <= x <= 1.0)
        ]
        
        for name, value, validator in config_items:
            valid = validator(value)
            success &= test_result(valid, f"{name}: {value} ({'Valid' if valid else 'Check config'})")
    
    except Exception as e:
        success = False
        test_result(False, f"Trading readiness check failed: {str(e)[:100]}")
    
    return success

def run_comprehensive_tests():
    """Run all tests and provide summary"""
    print("🤖 DogeBot Comprehensive Test Suite")
    print("====================================")
    print("Testing all components for production readiness...\n")
    
    test_functions = [
        test_1_environment_variables,
        test_2_account_connectivity, 
        test_3_order_manager,
        test_4_strategy_engine,
        test_5_docker_container,
        test_6_websocket_data,
        test_7_trading_readiness
    ]
    
    results = []
    for test_func in test_functions:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            results.append(False)
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print(f"\n{'='*60}")
    print("🎯 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! DogeBot is ready for production!")
        print("🚀 Your bot is fully operational and ready for 24/7 trading!")
    elif passed >= total * 0.8:
        print(f"\n⚠️  Most tests passed ({passed}/{total}). Minor issues detected.")
        print("🔧 Review failed tests and fix before production deployment.")
    else:
        print(f"\n🚨 Multiple test failures ({total-passed}/{total}). Critical issues detected.")
        print("🛠️  Fix failed components before deploying to production.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_comprehensive_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        traceback.print_exc()
        sys.exit(1)
