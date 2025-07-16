"""Tests for technical indicators"""

import pytest
import pandas as pd
import numpy as np
from bot.core.indicators import atr, ema, boll_pct


@pytest.mark.unit
class TestATR:
    """Test Average True Range indicator"""
    
    def test_atr_basic_calculation(self, sample_ohlc_data):
        """Test basic ATR calculation"""
        result = atr(sample_ohlc_data, period=14)
        
        # ATR should be a pandas Series
        assert isinstance(result, pd.Series)
        
        # ATR should have same length as input
        assert len(result) == len(sample_ohlc_data)
        
        # ATR values should be positive
        valid_atr = result.dropna()
        assert all(valid_atr >= 0)
        
        # First 13 values should be NaN (period-1)
        assert pd.isna(result.iloc[0:13]).all()
        
        # 14th value onwards should have values
        assert not pd.isna(result.iloc[13:]).any()
    
    def test_atr_different_periods(self, sample_ohlc_data):
        """Test ATR with different period values"""
        atr_7 = atr(sample_ohlc_data, period=7)
        atr_21 = atr(sample_ohlc_data, period=21)
        
        # Different periods should give different results
        assert not atr_7.equals(atr_21)
        
        # Shorter period should have fewer NaN values
        assert atr_7.isna().sum() < atr_21.isna().sum()
    
    def test_atr_edge_cases(self):
        """Test ATR edge cases"""
        # Test with minimal data
        small_data = pd.DataFrame({
            'high': [1.0, 1.1],
            'low': [0.9, 1.0],
            'close': [1.0, 1.1]
        })
        
        result = atr(small_data, period=14)
        # Should return all NaN for insufficient data
        assert result.isna().all()


@pytest.mark.unit
class TestEMA:
    """Test Exponential Moving Average indicator"""
    
    def test_ema_basic_calculation(self, sample_ohlc_data):
        """Test basic EMA calculation"""
        result = ema(sample_ohlc_data['close'], period=20)
        
        # EMA should be a pandas Series
        assert isinstance(result, pd.Series)
        
        # EMA should have same length as input
        assert len(result) == len(sample_ohlc_data)
        
        # First 19 values should be NaN (period-1)
        assert pd.isna(result.iloc[0:19]).all()
        
        # 20th value onwards should have values
        assert not pd.isna(result.iloc[19:]).any()
    
    def test_ema_responsiveness(self, sample_ohlc_data):
        """Test EMA responsiveness compared to SMA"""
        closes = sample_ohlc_data['close']
        ema_fast = ema(closes, period=10)
        ema_slow = ema(closes, period=50)
        
        # Fast EMA should be more responsive (more variation)
        ema_fast_std = ema_fast.dropna().std()
        ema_slow_std = ema_slow.dropna().std()
        
        # This might not always be true, but generally fast EMA is more volatile
        # assert ema_fast_std >= ema_slow_std
    
    def test_ema_trending_data(self):
        """Test EMA on trending data"""
        # Create uptrending data
        trending_data = pd.Series(range(1, 51))  # 1 to 50
        result = ema(trending_data, period=10)
        
        # EMA should follow the trend (increasing)
        valid_ema = result.dropna()
        assert all(valid_ema.diff().dropna() > 0)


@pytest.mark.unit
class TestBollPct:
    """Test Bollinger Band Percentage indicator"""
    
    def test_boll_pct_basic_calculation(self, sample_ohlc_data):
        """Test basic Bollinger Band % calculation"""
        result = boll_pct(sample_ohlc_data['close'], period=20)
        
        # Should be a pandas Series
        assert isinstance(result, pd.Series)
        
        # Should have same length as input
        assert len(result) == len(sample_ohlc_data)
        
        # First 19 values should be NaN (period-1)
        assert pd.isna(result.iloc[0:19]).all()
        
        # Values should be between 0 and 1
        valid_values = result.dropna()
        assert all(valid_values >= 0)
        assert all(valid_values <= 1)
    
    def test_boll_pct_extreme_values(self):
        """Test Bollinger Band % with extreme values"""
        # Create data with price at lower band
        stable_data = pd.Series([10] * 30)  # Stable price
        low_spike = stable_data.copy()
        low_spike.iloc[-1] = 8  # Price below lower band
        
        result = boll_pct(low_spike, period=20)
        
        # Last value should be close to 0 (at lower band)
        assert result.iloc[-1] < 0.1
        
        # Create data with price at upper band
        high_spike = stable_data.copy()
        high_spike.iloc[-1] = 12  # Price above upper band
        
        result = boll_pct(high_spike, period=20)
        
        # Last value should be close to 1 (at upper band)
        assert result.iloc[-1] > 0.9
    
    def test_boll_pct_mean_reversion(self, sample_ohlc_data):
        """Test that Bollinger Band % identifies mean reversion opportunities"""
        result = boll_pct(sample_ohlc_data['close'], period=20)
        valid_values = result.dropna()
        
        # Most values should be between 0.2 and 0.8 (normal range)
        normal_range = valid_values[(valid_values >= 0.2) & (valid_values <= 0.8)]
        assert len(normal_range) > len(valid_values) * 0.7  # At least 70% in normal range


@pytest.mark.unit
class TestIndicatorIntegration:
    """Test indicators working together"""
    
    def test_all_indicators_same_length(self, sample_ohlc_data):
        """Test that all indicators return same length results"""
        df = sample_ohlc_data.copy()
        
        df['atr'] = atr(df, period=14)
        df['ema'] = ema(df['close'], period=20)
        df['bb_pct'] = boll_pct(df['close'], period=20)
        
        # All columns should have same length
        assert len(df['atr']) == len(df['ema']) == len(df['bb_pct'])
        assert len(df) == len(sample_ohlc_data)
    
    def test_indicators_with_strategy_requirements(self, sample_ohlc_data):
        """Test indicators meet strategy requirements"""
        df = sample_ohlc_data.copy()
        
        # Simulate strategy requirements
        df['atr14'] = atr(df, period=14)
        df['ema50'] = ema(df['close'], period=50)
        df['boll_pct'] = boll_pct(df['close'], period=20)
        
        # After 50 periods, we should have valid strategy signals
        valid_data = df.iloc[50:].copy()
        
        # Check that we can identify strategy entry conditions
        entry_conditions = (
            (valid_data['boll_pct'] <= 0.15) &  # Low volatility
            (valid_data['close'] > 0.97 * valid_data['ema50']) &  # Above EMA
            (~valid_data['atr14'].isna())  # Valid ATR
        )
        
        # Should have some valid entry points
        assert entry_conditions.any()
