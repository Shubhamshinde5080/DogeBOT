"""Pytest fixtures for DogeBot tests"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_ohlc_data():
    """Generate sample OHLC data for testing indicators"""
    np.random.seed(42)  # For reproducible tests
    
    # Generate 100 data points
    n = 100
    base_price = 100.0
    
    # Create realistic price movement
    returns = np.random.normal(0, 0.02, n)  # 2% daily volatility
    prices = [base_price]
    
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Create OHLC from price series
    data = []
    for i, close in enumerate(prices):
        # Add some intraday volatility
        high_mult = 1 + abs(np.random.normal(0, 0.01))
        low_mult = 1 - abs(np.random.normal(0, 0.01))
        
        high = close * high_mult
        low = close * low_mult
        
        # Open is close of previous period (or base for first)
        open_price = prices[i-1] if i > 0 else base_price
        
        data.append({
            'open': open_price,
            'high': max(open_price, high, close),
            'low': min(open_price, low, close),
            'close': close
        })
    
    return pd.DataFrame(data)


@pytest.fixture
def mock_kline_message():
    """Sample WebSocket kline message from Binance"""
    return {
        "e": "kline",
        "E": 1699123456789,
        "s": "DOGEFDUSD",
        "k": {
            "t": 1699123200000,  # Open time
            "T": 1699124099999,  # Close time
            "s": "DOGEFDUSD",
            "i": "15m",
            "f": 12345,
            "L": 12399,
            "o": "0.08500",  # Open price
            "c": "0.08550",  # Close price
            "h": "0.08600",  # High price
            "l": "0.08480",  # Low price
            "v": "1000000",  # Volume
            "n": 55,
            "x": True,       # Is closed
            "q": "85000",
            "V": "500000",
            "Q": "42500",
            "B": "0"
        }
    }
