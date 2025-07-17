import numpy as np
import pandas as pd

def atr(df: pd.DataFrame, win: int = 14) -> pd.Series:
    # Safety check: need enough data for ATR calculation
    if len(df) < win:
        return pd.Series([np.nan] * len(df), index=df.index)
    
    tr = np.maximum.reduce([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift()).abs(),
        (df['low'] - df['close'].shift()).abs()
    ])
    return pd.Series(tr, index=df.index).rolling(win).mean()

def boll_pct(df: pd.DataFrame, win: int = 20, dev: int = 2) -> pd.Series:
    # Safety check: need enough data for Bollinger calculation  
    if len(df) < win:
        return pd.Series([np.nan] * len(df), index=df.index)
        
    mb = df['close'].rolling(win).mean()
    sd = df['close'].rolling(win).std()
    upper = mb + dev*sd
    lower = mb - dev*sd
    return (df['close'] - lower)/(upper - lower)

def ema(series: pd.Series, span: int = 200) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def vwap(df: pd.DataFrame) -> pd.Series:
    """Volume Weighted Average Price"""
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    return (typical_price * df['volume']).cumsum() / df['volume'].cumsum()

def vwap(prices, qtys):
    return (np.array(prices)*np.array(qtys)).sum() / np.array(qtys).sum()