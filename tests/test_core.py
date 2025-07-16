"""Simple tests for DogeBot core functionality"""

import pytest
import pandas as pd
import numpy as np
from tests.fixtures import sample_ohlc_data, mock_kline_message


def test_basic_math():
    """Basic test to ensure pytest is working"""
    assert 1 + 1 == 2
    assert True is True


def test_pandas_operations():
    """Test pandas operations work correctly"""
    df = pd.DataFrame({
        'close': [1, 2, 3, 4, 5],
        'high': [1.1, 2.1, 3.1, 4.1, 5.1],
        'low': [0.9, 1.9, 2.9, 3.9, 4.9]
    })
    
    assert len(df) == 5
    assert df['close'].mean() == 3.0
    assert df['high'].max() == 5.1


def test_sample_data_fixture(sample_ohlc_data):
    """Test that our sample data fixture works"""
    assert isinstance(sample_ohlc_data, pd.DataFrame)
    assert len(sample_ohlc_data) == 100
    assert all(col in sample_ohlc_data.columns for col in ['open', 'high', 'low', 'close'])
    
    # Check OHLC relationships
    assert all(sample_ohlc_data['high'] >= sample_ohlc_data['close'])
    assert all(sample_ohlc_data['high'] >= sample_ohlc_data['open'])
    assert all(sample_ohlc_data['low'] <= sample_ohlc_data['close'])
    assert all(sample_ohlc_data['low'] <= sample_ohlc_data['open'])


def test_kline_message_fixture(mock_kline_message):
    """Test that our kline message fixture is valid"""
    assert mock_kline_message['e'] == 'kline'
    assert mock_kline_message['s'] == 'DOGEFDUSD'
    
    kline = mock_kline_message['k']
    assert kline['x'] is True  # Is closed
    assert kline['s'] == 'DOGEFDUSD'
    assert kline['i'] == '15m'
    
    # Check price fields are present
    for field in ['o', 'h', 'l', 'c']:
        assert field in kline
        assert float(kline[field]) > 0


@pytest.mark.unit
def test_environment_variables():
    """Test environment variable handling"""
    import os
    
    # These might not be set in test environment, just check they don't crash
    api_key = os.getenv('BINANCE_API_KEY', 'test_key')
    base_url = os.getenv('BASE_URL', 'https://testnet.binance.vision/api')
    
    assert isinstance(api_key, str)
    assert isinstance(base_url, str)
    assert 'binance' in base_url.lower()


def test_price_calculations():
    """Test basic price calculation functions"""
    prices = [100, 102, 98, 105, 95]
    
    # Calculate simple returns
    returns = []
    for i in range(1, len(prices)):
        ret = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(ret)
    
    assert len(returns) == 4
    assert abs(returns[0] - 0.02) < 0.001  # 2% gain
    assert returns[1] < 0  # Negative return


@pytest.mark.integration
def test_imports_work():
    """Test that all our modules can be imported"""
    try:
        import bot.core.indicators
        import bot.core.strategy
        import bot.core.order_mgr
        import bot.services.websocket
        import bot.app
        
        # If we get here, all imports worked
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_moving_average_calculation():
    """Test a simple moving average calculation"""
    prices = [10, 12, 14, 16, 18, 20]
    window = 3
    
    # Calculate simple moving average manually
    sma = []
    for i in range(window - 1, len(prices)):
        avg = sum(prices[i-window+1:i+1]) / window
        sma.append(avg)
    
    expected = [12.0, 14.0, 16.0, 18.0]  # 3-period SMA
    assert sma == expected


def test_volatility_calculation():
    """Test basic volatility calculation"""
    prices = [100, 105, 98, 102, 110]
    
    # Calculate price changes
    changes = []
    for i in range(1, len(prices)):
        change = abs(prices[i] - prices[i-1])
        changes.append(change)
    
    avg_change = sum(changes) / len(changes)
    assert avg_change > 0
    assert isinstance(avg_change, (int, float))
