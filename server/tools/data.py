from pathlib import Path
import pandas as pd
import yfinance as yf

DATA_DIR = Path("stock_data")
DATA_DIR.mkdir(exist_ok=True)


def load_stock_data(symbol, period="1y", interval="1d"):

    csv_path = DATA_DIR / f"{symbol}_{period}_{interval}.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path, index_col=0, parse_dates=True), csv_path

    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=True,
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    df.to_csv(csv_path)

    return df, csv_path