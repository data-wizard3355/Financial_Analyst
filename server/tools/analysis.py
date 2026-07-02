import numpy as np


def analyze_dataframe(symbol, df):

    first = float(df["Close"].iloc[0])
    last = float(df["Close"].iloc[-1])

    returns = df["Close"].pct_change().dropna()

    return {

        "symbol": symbol,
        "start_date": str(df.index.min().date()),
        "end_date": str(df.index.max().date()),

        "period_high": float(df["High"].max()),
        "period_low": float(df["Low"].min()),

        "first_close": first,
        "last_close": last,

        "pct_change": round((last-first)/first*100,2),

        "avg_volume": float(df["Volume"].mean()),

        "mean_close": float(df["Close"].mean()),

        "median_close": float(df["Close"].median()),

        "std_dev": float(df["Close"].std()),

        "volatility": float(returns.std()*np.sqrt(252)),

        "52_week_high": float(df["High"].max()),

        "52_week_low": float(df["Low"].min())
    }

import pandas as pd

def correlation_analysis(stock_data):

    closes = {}
    for symbol, df in stock_data.items():
        closes[symbol] = df["Close"]
    corr = pd.DataFrame(closes).corr()
    return corr.round(4).to_dict()

def create_stock_summary(df, symbol):

    first_close = float(df["Close"].iloc[0])
    last_close = float(df["Close"].iloc[-1])
    pct_change = (
        (last_close - first_close)
        / first_close
    ) * 100

    return {
        "symbol": symbol,
        "period_high": float(df["High"].max()),
        "period_low": float(df["Low"].min()),
        "average_volume": float(df["Volume"].mean()),
        "trading_days": len(df),
        "pct_change": round(pct_change, 2),
        "start_date": str(df.index.min().date()),
        "end_date": str(df.index.max().date())
    }