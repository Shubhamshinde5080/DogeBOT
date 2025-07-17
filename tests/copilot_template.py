"""
🚀 PERFECT GITHUB COPILOT TEST TEMPLATE
Copy this EXACT template and give it to GitHub Copilot!
"""

# ============================================================================
# 📋 TELL GITHUB COPILOT EXACTLY THIS:
# ============================================================================

"""
Create pytest unit tests for my DogeBot with REAL assertions, not print statements. 

REQUIREMENTS:
1. assert bb_value <= 0.30 - actual BB calculation verification
2. assert price > 0.95 * ema_value - real EMA condition testing  
3. assert drop_percent >= 0.02 - mathematical drop verification
4. Use mock data with known expected results
5. NO print statements - only assert statements
6. Test both success AND failure scenarios
7. Follow this EXACT template structure

TEMPLATE TO FOLLOW:
"""

import pytest
import pandas as pd
import numpy as np

def test_my_dogebot_function():
    """REAL TEST - no print statements allowed!"""
    
    # ========================================
    # ARRANGE: Create test data with known results
    # ========================================
    
    # Create test data that WILL produce expected results
    test_data = pd.DataFrame({
        'high':   [1.001, 1.002, 1.003],  # Known values
        'low':    [0.999, 1.000, 1.001],
        'close':  [1.000, 1.001, 1.002],
        'volume': [1000000, 1000000, 1000000]
    })
    
    # ========================================
    # ACT: Run the function under test
    # ========================================
    
    # Calculate your indicator/condition
    result = my_indicator_function(test_data)
    
    # Get the specific value to test
    final_value = result.iat[-1]
    
    # ========================================
    # ASSERT: Verify the results - NO PRINT STATEMENTS!
    # ========================================
    
    # Check the result is valid
    assert not pd.isna(final_value), "Result should not be NaN"
    assert isinstance(final_value, (float, int, np.float64)), "Result should be numeric"
    
    # Check the business logic condition
    assert final_value <= 0.30, f"Expected value ≤ 0.30, got {final_value:.3f}"
    assert final_value >= 0.00, f"Value should be non-negative, got {final_value:.3f}"

def test_my_dogebot_failure_case():
    """REAL TEST - verify failure conditions"""
    
    # ARRANGE: Create data that should FAIL the condition
    bad_test_data = create_high_volatility_data()
    
    # ACT: Run the function
    result = my_indicator_function(bad_test_data)
    final_value = result.iat[-1]
    
    # ASSERT: Verify it correctly fails
    assert final_value > 0.30, f"High volatility should give value > 0.30, got {final_value:.3f}"

# ============================================================================
# 🎯 SPECIFIC DOGEBOT EXAMPLES FOR COPILOT:
# ============================================================================

def test_bollinger_band_low_volatility():
    """Test BB ≤ 0.30 condition with controlled data"""
    
    # ARRANGE: Create extremely stable price data
    stable_prices = [0.21000] * 25  # Flat prices = low volatility
    test_df = pd.DataFrame({
        'high':   [p + 0.000001 for p in stable_prices],  # Tiny spreads
        'low':    [p - 0.000001 for p in stable_prices],
        'close':  stable_prices,
        'volume': [1000000] * 25
    })
    
    # ACT: Calculate Bollinger Band %
    from bot.core.indicators import boll_pct
    bb_result = boll_pct(test_df, win=20)
    bb_value = bb_result.iat[-1]
    
    # ASSERT: Verify low volatility condition
    assert not pd.isna(bb_value), "BB should be calculated"
    assert bb_value <= 0.30, f"Low volatility should give BB ≤ 0.30, got {bb_value:.3f}"

def test_ema_above_condition():
    """Test price > 95% EMA condition"""
    
    # ARRANGE: Create uptrending data  
    base_price = 0.21000
    uptrend_prices = [base_price + i * 0.0001 for i in range(60)]
    
    test_df = pd.DataFrame({
        'high':   [p * 1.001 for p in uptrend_prices],
        'low':    [p * 0.999 for p in uptrend_prices],
        'close':  uptrend_prices,
        'volume': [1000000] * 60
    })
    
    # ACT: Calculate EMA
    from bot.core.indicators import ema
    ema_result = ema(test_df['close'], span=50)
    
    current_price = test_df['close'].iat[-1]
    ema_value = ema_result.iat[-1]
    ratio = current_price / ema_value
    
    # ASSERT: Verify EMA condition
    assert not pd.isna(ema_value), "EMA should be calculated"
    assert current_price > 0.95 * ema_value, f"Price should be > 95% EMA, ratio: {ratio:.4f}"
    assert ratio >= 0.95, f"Expected ratio ≥ 0.95, got {ratio:.4f}"

def test_drop_detection():
    """Test 2% drop detection logic"""
    
    # ARRANGE: Create data with known drop
    stable_price = 0.21000
    spike_price = stable_price * 1.03   # 3% spike
    drop_price = spike_price * 0.975    # 2.5% drop from spike
    
    prices = [stable_price] * 20 + [spike_price, drop_price]
    
    test_df = pd.DataFrame({
        'high':   [p * 1.001 for p in prices],
        'low':    [p * 0.999 for p in prices], 
        'close':  prices,
        'volume': [1000000] * len(prices)
    })
    
    # ACT: Calculate drop percentage (like in your websocket.py)
    recent_high = test_df['high'].tail(4).max()
    current_price = test_df['close'].iat[-1]
    drop_percent = (recent_high - current_price) / recent_high
    
    # ASSERT: Verify drop detection
    assert drop_percent >= 0.02, f"Should detect ≥2% drop, got {drop_percent:.3f}"
    assert drop_percent <= 0.05, f"Drop too large for test, got {drop_percent:.3f}"

# ============================================================================
# ❌ WHAT NOT TO DO (Show Copilot this as BAD example):
# ============================================================================

def bad_test_example():
    """BAD TEST - Don't write tests like this!"""
    print("Testing DogeBot...")           # ❌ NO PRINT STATEMENTS!
    print("Checking conditions...")        # ❌ NOT TESTING ANYTHING!
    print("All tests passed!")            # ❌ FAKE SUCCESS!
    return True                           # ❌ NO VERIFICATION!

# ============================================================================
# ✅ WHAT TO DO (Show Copilot this as GOOD example):
# ============================================================================

def good_test_example():
    """GOOD TEST - Write tests like this!"""
    # ARRANGE
    test_input = create_test_data()
    
    # ACT  
    result = calculate_something(test_input)
    
    # ASSERT - REAL VERIFICATION!
    assert result == expected_value, f"Expected {expected_value}, got {result}"
    assert isinstance(result, float), "Result should be numeric"
    assert result > 0, "Result should be positive"
    # NO PRINT STATEMENTS!

# ============================================================================
# 📝 COPY THIS EXACT MESSAGE TO GITHUB COPILOT:
# ============================================================================

"""
GitHub Copilot, create tests for my DogeBot that follow this pattern:

1. Use pytest framework
2. Create test data with known expected outcomes  
3. Use real assert statements, not print statements
4. Test specific conditions: BB ≤ 0.30, EMA > 95%, drop ≥ 2%
5. Include both success and failure test cases
6. Follow the Arrange-Act-Assert pattern
7. Make assertions specific with error messages
8. Return None from test functions (don't return True/False)

Example structure:
```python
def test_specific_condition():
    # ARRANGE: Create known test data
    test_data = create_controlled_data()
    
    # ACT: Run the function
    result = my_function(test_data)
    
    # ASSERT: Verify with specific checks
    assert condition_met, f"Expected X, got {result}"
```

Do NOT use print statements. Only use assert statements for verification.
"""

if __name__ == "__main__":
    print("📋 Copy the template above and give it to GitHub Copilot!")
    print("🚀 This will make Copilot write REAL tests with assertions!")
    print("✅ No more fake print statement tests!")
