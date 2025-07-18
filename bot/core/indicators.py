import numpy as np
import pandas as pd

def atr(df: pd.DataFrame, win: int = 14) -> pd.Series:
    # Safety check: need enough data for ATR calculation
    if len(df) < win:
        return pd.Series([np.nan] * len(df), index=df.index)
    
    # Suppress the NumPy warning about NaN values in the first few rows
    with np.errstate(invalid='ignore'):
        tr = np.maximum.reduce([
            df['high'] - df['low'],
            (df['high'] - df['close'].shift()).abs(),
            (df['low'] - df['close'].shift()).abs()
        ])
    
    # Calculate rolling mean and forward-fill NaN values for early periods
    atr_series = pd.Series(tr, index=df.index).rolling(win).mean()
    
    # For the first few NaN periods, use a simple average of available true range values
    if len(df) >= 2:  # Need at least 2 candles for basic ATR
        first_valid_idx = atr_series.first_valid_index()
        if first_valid_idx is not None:
            # Fill earlier NaN values with the first valid ATR value
            atr_series = atr_series.bfill()
            
    return atr_series

def boll_pct(df: pd.DataFrame, win: int = 20, dev: int = 2) -> pd.Series:
    # Safety check: need enough data for Bollinger calculation  
    if len(df) < win:
        return pd.Series([np.nan] * len(df), index=df.index)
        
    mb = df['close'].rolling(win, min_periods=1).mean()
    sd = df['close'].rolling(win, min_periods=1).std()
    upper = mb + dev*sd
    lower = mb - dev*sd
    return (df['close'] - lower)/(upper - lower)

def ema(series: pd.Series, span: int = 200) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def vwap(df: pd.DataFrame) -> pd.Series:
    """Volume Weighted Average Price"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    return (typical_price * df['volume']).cumsum() / df['volume'].cumsum()

def vwap_list(prices, qtys):
    return (np.array(prices)*np.array(qtys)).sum() / np.array(qtys).sum()
