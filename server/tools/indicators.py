import pandas as pd


def calculate_indicators_dataframe(symbol: str, df: pd.DataFrame) -> dict:
    """
    Calculate commonly used technical indicators for a stock.

    This function operates entirely on an existing DataFrame and does not
    download any data. It is intended to be used after load_stock_data()
    has already retrieved the historical prices.

    Indicators calculated:
    ----------------------
    - Current Closing Price
    - SMA 20
    - SMA 50
    - EMA 20
    - RSI (14)
    - MACD
    - MACD Signal
    - MACD Histogram
    - Bollinger Bands (20)

    Parameters
    ----------
    symbol : str
        Stock ticker.

    df : pandas.DataFrame
        Historical OHLCV dataframe.

    Returns
    -------
    dict
        Dictionary containing the latest values of all indicators.
    """

    close = df["Close"]

    # ----------------------------
    # Moving Averages
    # ----------------------------

    sma20 = close.rolling(20).mean()

    sma50 = close.rolling(50).mean()

    ema20 = close.ewm(span=20, adjust=False).mean()

    # ----------------------------
    # RSI (14)
    # ----------------------------

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    # ----------------------------
    # MACD
    # ----------------------------

    ema12 = close.ewm(span=12, adjust=False).mean()

    ema26 = close.ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26

    signal = macd.ewm(span=9, adjust=False).mean()

    histogram = macd - signal

    # ----------------------------
    # Bollinger Bands
    # ----------------------------

    middle = sma20

    std = close.rolling(20).std()

    upper = middle + (2 * std)

    lower = middle - (2 * std)

    return {
        "symbol": symbol,

        "current_price": round(float(close.iloc[-1]), 2),

        "sma20": round(float(sma20.iloc[-1]), 2),
        "sma50": round(float(sma50.iloc[-1]), 2),
        "ema20": round(float(ema20.iloc[-1]), 2),

        "rsi": round(float(rsi.iloc[-1]), 2),

        "macd": round(float(macd.iloc[-1]), 2),
        "macd_signal": round(float(signal.iloc[-1]), 2),
        "macd_histogram": round(float(histogram.iloc[-1]), 2),

        "bollinger_upper": round(float(upper.iloc[-1]), 2),
        "bollinger_middle": round(float(middle.iloc[-1]), 2),
        "bollinger_lower": round(float(lower.iloc[-1]), 2),
    }