"""Test configuration and fixtures for DogeBot test suite"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch


@pytest.fixture
def sample_ohlc_data():
    """Generate sample OHLC data for testing indicators"""
    np.random.seed(42)  # For reproducible tests
    
    dates = pd.date_range('2024-01-01', periods=100, freq='15min')
    
    # Generate realistic OHLC data
    closes = np.cumsum(np.random.randn(100) * 0.001) + 0.08  # Starting around $0.08
    opens = closes + np.random.randn(100) * 0.0005
    highs = np.maximum(opens, closes) + np.abs(np.random.randn(100) * 0.001)
    lows = np.minimum(opens, closes) - np.abs(np.random.randn(100) * 0.001)
    
    return pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes
    }, index=dates)


@pytest.fixture
def mock_binance_client():
    """Mock Binance client for testing"""
    with patch('binance.client.Client') as mock:
        yield mock


@pytest.fixture
def mock_websocket():
    """Mock WebSocket client for testing"""
    with patch('binance.websocket.spot.websocket_stream.SpotWebsocketStreamClient') as mock:
        yield mock


@pytest.fixture
def sample_kline_message():
    """Sample WebSocket kline message for testing"""
    return {
        "e": "kline",
        "E": 1640995200000,
        "s": "DOGEFDUSD",
        "k": {
            "t": 1640995200000,  # Kline start time
            "T": 1640996099999,  # Kline close time
            "s": "DOGEFDUSD",     # Symbol
            "i": "15m",          # Interval
            "f": 100,            # First trade ID
            "L": 200,            # Last trade ID
            "o": "0.08000",      # Open price
            "c": "0.08050",      # Close price
            "h": "0.08100",      # High price
            "l": "0.07950",      # Low price
            "v": "1000",         # Base asset volume
            "n": 100,            # Number of trades
            "x": True,           # Is this kline closed?
            "q": "80.5",         # Quote asset volume
            "V": "500",          # Taker buy base asset volume
            "Q": "40.25"         # Taker buy quote asset volume
        }
    }
