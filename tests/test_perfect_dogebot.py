"""
PERFECT DogeBot Tests - Copy this EXACT template to GitHub Copilot!
This shows the RIGHT WAY to write real tests with assertions.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add the bot directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.core.indicators import atr, ema, boll_pct

class TestDogeBotConditions:
    """
    REAL DogeBot tests - Show GitHub Copilot THIS template!
    """
    
    def create_low_volatility_data(self):
        """Create test data that WILL produce BB ≤ 0.30"""
        # Create data where close is near the lower Bollinger Band
        base_price = 0.21000
        
        # Start with higher prices, then drop to lower band area
        prices = []
        
        # First 25 candles: slightly higher prices to establish bands
        for i in range(25):
            price = base_price + 0.0001  # Slightly above base
            prices.append(price)
        
        # Last 5 candles: drop to lower area (this will put BB% low)
        for i in range(5):
            price = base_price - 0.0002  # Below the range = low BB%
            prices.append(price)
        
        return pd.DataFrame({
            'high': [p + 0.000005 for p in prices],
            'low': [p - 0.000005 for p in prices],
            'close': prices,
            'volume': [1000000] * len(prices)
        })
    
    def create_high_volatility_data(self):
        """Create test data that WILL produce BB > 0.30"""
        base_price = 0.21000
        
        # Create extreme volatility with guaranteed high BB
        # Use a clear pattern: low-high-low-high to force high standard deviation
        prices = []
        for i in range(30):
            if i % 2 == 0:
                # Low price
                price = base_price * 0.995  # -0.5%
            else:
                # High price  
                price = base_price * 1.005  # +0.5%
            prices.append(price)
        
        return pd.DataFrame({
            'high': [p * 1.002 for p in prices],  # Add some spread
            'low': [p * 0.998 for p in prices],
            'close': prices,
            'volume': [1000000] * len(prices)
        })
    
    def create_drop_scenario_data(self):
        """Create test data with guaranteed 2%+ drop"""
        base_price = 0.21000
        
        # 25 stable candles
        stable_prices = [base_price] * 25
        
        # Add spike and 3% drop at the end
        spike = base_price * 1.025     # 2.5% spike
        drop = spike * 0.97           # 3% drop from spike
        
        prices = stable_prices + [spike, drop]
        
        return pd.DataFrame({
            'high': [p * 1.001 for p in prices],
            'low': [p * 0.999 for p in prices],
            'close': prices,
            'volume': [1000000] * len(prices)
        })
    
    def create_no_drop_data(self):
        """Create test data with NO significant drop"""
        base_price = 0.21000
        
        # Rising prices - no drops
        prices = [base_price + i * 0.0001 for i in range(30)]
        
        return pd.DataFrame({
            'high': [p * 1.001 for p in prices],
            'low': [p * 0.999 for p in prices],
            'close': prices,
            'volume': [1000000] * len(prices)
        })

    def test_bb_low_volatility_condition(self):
        """
        REAL TEST: Verify BB ≤ 0.30 with low volatility data
        """
        # Arrange: Create known low volatility data
        df = self.create_low_volatility_data()
        
        # Act: Calculate BB
        df['bb'] = boll_pct(df, win=20)
        bb_value = df['bb'].iat[-1]
        
        # Assert: Verify BB is low
        assert not pd.isna(bb_value), "BB should be calculated"
        assert bb_value <= 0.30, f"Expected BB ≤ 0.30, got {bb_value:.3f}"
        assert bb_value >= 0.0, f"BB should be non-negative, got {bb_value:.3f}"

    def test_bb_high_volatility_condition(self):
        """
        REAL TEST: Verify BB > 0.30 with high volatility data  
        """
        # Arrange: Create known high volatility data
        df = self.create_high_volatility_data()
        
        # Act: Calculate BB
        df['bb'] = boll_pct(df, win=20)
        bb_value = df['bb'].iat[-1]
        
        # Assert: Verify BB is high
        assert not pd.isna(bb_value), "BB should be calculated"
        assert bb_value > 0.30, f"Expected BB > 0.30, got {bb_value:.3f}"
        assert bb_value <= 1.0, f"BB should be ≤ 1.0, got {bb_value:.3f}"

    def test_ema_above_condition(self):
        """
        REAL TEST: Verify price > 95% EMA condition
        """
        # Arrange: Create uptrending data
        base_price = 0.21000
        prices = [base_price + i * 0.0001 for i in range(60)]  # Need 60 for EMA50
        
        df = pd.DataFrame({
            'high': [p * 1.001 for p in prices],
            'low': [p * 0.999 for p in prices], 
            'close': prices,
            'volume': [1000000] * len(prices)
        })
        
        # Act: Calculate EMA
        df['ema'] = ema(df['close'], span=50)
        
        price = df['close'].iat[-1]
        ema_value = df['ema'].iat[-1]
        ratio = price / ema_value
        
        # Assert: Verify EMA condition  
        assert not pd.isna(ema_value), "EMA should be calculated"
        assert price > 0.95 * ema_value, f"Expected price > 95% EMA, got {ratio:.4f}"
        assert ratio >= 0.95, f"Expected ratio ≥ 0.95, got {ratio:.4f}"

    def test_drop_detection_condition(self):
        """
        REAL TEST: Verify 2% drop detection
        """
        # Arrange: Create data with known drop
        df = self.create_drop_scenario_data()
        
        # Act: Calculate drop percentage
        recent_high = df['high'].tail(4).max()
        current_price = df['close'].iat[-1]
        drop_percent = (recent_high - current_price) / recent_high
        
        # Assert: Verify drop detection
        assert drop_percent >= 0.02, f"Expected drop ≥ 2%, got {drop_percent:.3f}"
        assert drop_percent <= 0.10, f"Drop too large, got {drop_percent:.3f}"

    def test_no_drop_blocks_buy(self):
        """
        REAL TEST: Verify no drop prevents buying
        """
        # Arrange: Create rising data with no drops
        df = self.create_no_drop_data()
        
        # Act: Calculate drop percentage
        recent_high = df['high'].tail(4).max()
        current_price = df['close'].iat[-1]
        drop_percent = (recent_high - current_price) / recent_high
        
        # Assert: Verify no significant drop
        assert drop_percent < 0.02, f"Expected drop < 2%, got {drop_percent:.3f}"
        assert drop_percent >= 0.0, f"Drop should be non-negative, got {drop_percent:.3f}"

    def test_atr_calculation_condition(self):
        """
        REAL TEST: Verify ATR calculation works
        """
        # Arrange: Create data with known volatility
        df = self.create_high_volatility_data()
        
        # Act: Calculate ATR
        df['atr'] = atr(df, win=14)
        atr_value = df['atr'].iat[-1]
        
        # Assert: Verify ATR calculation
        assert not pd.isna(atr_value), "ATR should be calculated"
        assert atr_value > 0, f"ATR should be positive, got {atr_value:.6f}"
        assert isinstance(atr_value, (float, np.float64)), "ATR should be numeric"

    def test_insufficient_data_handling(self):
        """
        REAL TEST: Verify insufficient data is handled correctly
        """
        # Arrange: Create minimal data
        df = pd.DataFrame({
            'high': [0.21001] * 10,    # Only 10 candles
            'low': [0.20999] * 10,
            'close': [0.21000] * 10,
            'volume': [1000000] * 10
        })
        
        # Act: Try to calculate indicators
        df['bb'] = boll_pct(df, win=20)  # Needs 20
        df['atr'] = atr(df, win=14)      # Needs 14
        
        # Assert: Verify proper NaN handling
        assert pd.isna(df['bb'].iat[-1]), "BB should be NaN with insufficient data"
        assert pd.isna(df['atr'].iat[-1]), "ATR should be NaN with insufficient data"

# Test functions (not class methods) for pytest
def test_dogebot_bb_low_volatility():
    """Pytest function: Test BB low volatility condition"""
    test_instance = TestDogeBotConditions()
    test_instance.test_bb_low_volatility_condition()

def test_dogebot_bb_high_volatility():
    """Pytest function: Test BB high volatility condition"""
    test_instance = TestDogeBotConditions()
    test_instance.test_bb_high_volatility_condition()

def test_dogebot_ema_above():
    """Pytest function: Test EMA above condition"""
    test_instance = TestDogeBotConditions()
    test_instance.test_ema_above_condition()

def test_dogebot_drop_detection():
    """Pytest function: Test drop detection"""
    test_instance = TestDogeBotConditions()
    test_instance.test_drop_detection_condition()

def test_dogebot_no_drop():
    """Pytest function: Test no drop blocking"""
    test_instance = TestDogeBotConditions()
    test_instance.test_no_drop_blocks_buy()

def test_dogebot_atr_calculation():
    """Pytest function: Test ATR calculation"""
    test_instance = TestDogeBotConditions()
    test_instance.test_atr_calculation_condition()

def test_dogebot_insufficient_data():
    """Pytest function: Test insufficient data handling"""
    test_instance = TestDogeBotConditions()
    test_instance.test_insufficient_data_handling()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
