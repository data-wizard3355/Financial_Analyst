from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_price_chart(df, symbol):
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df["Close"], label="Close")
    plt.plot(df.index, df["SMA20"], label="20 SMA")
    plt.plot(df.index, df["SMA50"], label="50 SMA")
    plt.legend()
    plt.title(symbol)
    filename = OUTPUT_DIR / f"{symbol}_price.png"
    plt.savefig(filename,bbox_inches="tight")
    plt.close()
    return str(filename)


def generate_comparison_chart(stock_data):
    plt.figure(figsize=(12,6))
    for symbol, df in stock_data.items():
        normalized = df["Close"]/df["Close"].iloc[0]*100
        plt.plot(normalized,label=symbol)
    plt.legend()
    plt.title("Stock Comparison")
    filename = OUTPUT_DIR/"comparison.png"
    plt.savefig(filename,bbox_inches="tight")
    plt.close()
    return str(filename)

def generate_volume_chart(df, symbol):
    plt.figure(figsize=(12,6))
    plt.bar(df.index, df["Volume"])
    plt.title(f"{symbol} Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    filename = OUTPUT_DIR / f"{symbol}_volume.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    return str(filename)

def generate_ma_chart(df, symbol):
    df = df.copy()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df["MA20"], label="20 Day MA")
    plt.plot(df.index, df["MA50"], label="50 Day MA")
    plt.title(f"{symbol} Moving Averages")
    plt.legend()
    filename = OUTPUT_DIR / f"{symbol}_moving_average.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)

import mplfinance as mpf

def generate_candlestick_chart(df, symbol):
    filename = OUTPUT_DIR / f"{symbol}_candlestick.png"

    mpf.plot(
        df,
        type="candle",
        style="yahoo",
        volume=True,
        savefig=str(filename)
    )

    return str(filename)

def generate_rsi_chart(df, symbol):
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100/(1+rs))
    plt.figure(figsize=(12,5))
    plt.plot(df.index, rsi)
    plt.axhline(70, linestyle="--")
    plt.axhline(30, linestyle="--")
    plt.title(f"{symbol} RSI")
    filename = OUTPUT_DIR / f"{symbol}_rsi.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)

def generate_macd_chart(df, symbol):
    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    plt.figure(figsize=(12,6))
    plt.plot(df.index, macd, label="MACD")
    plt.plot(df.index, signal, label="Signal")
    plt.legend()
    plt.title(f"{symbol} MACD")
    filename = OUTPUT_DIR / f"{symbol}_macd.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)

import seaborn as sns

def generate_heatmap(stock_data):
    closes = {}
    for symbol, df in stock_data.items():
        closes[symbol] = df["Close"]
    corr = pd.DataFrame(closes).corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    filename = OUTPUT_DIR / "correlation_heatmap.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)


def generate_returns_chart(df, symbol):
    returns = df["Close"].pct_change()*100
    plt.figure(figsize=(12,5))
    plt.plot(df.index, returns)
    plt.title(f"{symbol} Daily Returns")
    filename = OUTPUT_DIR / f"{symbol}_returns.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)

def generate_volatility_chart(df, symbol):
    volatility = df["Close"].pct_change().rolling(20).std()*100
    plt.figure(figsize=(12,5))
    plt.plot(df.index, volatility)
    plt.title(f"{symbol} Rolling Volatility")
    filename = OUTPUT_DIR / f"{symbol}_volatility.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)

def generate_drawdown_chart(df, symbol):
    running_max = df["Close"].cummax()
    drawdown = (df["Close"] - running_max) / running_max * 100
    plt.figure(figsize=(12,5))
    plt.fill_between(df.index, drawdown, 0)
    plt.title(f"{symbol} Drawdown")
    filename = OUTPUT_DIR / f"{symbol}_drawdown.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight")
    plt.close()
    return str(filename)