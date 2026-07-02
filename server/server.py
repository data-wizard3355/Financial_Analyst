from mcp.server.fastmcp import FastMCP
from tools.data import load_stock_data
from tools.analysis import analyze_dataframe
from tools.charts import (
    generate_price_chart,
    generate_comparison_chart,
    generate_volume_chart,
    generate_ma_chart,
    generate_candlestick_chart,
    generate_rsi_chart,
    generate_macd_chart,
    generate_heatmap,
    generate_returns_chart,
    generate_volatility_chart,
    generate_drawdown_chart

)
from tools.pdf_report import generate_pdf
from tools.indicators import calculate_indicators_dataframe
from tools.analysis import create_stock_summary,correlation_analysis

mcp = FastMCP("Financial MCP Server")

@mcp.tool()
def get_stock_data(
    symbol: str,
    period: str = "1y",
    interval: str = "1d",
) -> str:
    """
    Retrieve historical stock market data for a given stock symbol.

    This tool acts as the primary data retrieval service for the Financial MCP
    Server. It first checks whether the requested dataset already exists in the
    local cache. If a cached file is available, it loads the existing data.
    Otherwise, it downloads the data from Yahoo Finance using the yfinance
    library and automatically caches it for future use.

    The returned dataset contains historical OHLCV (Open, High, Low, Close,
    Volume) data and can be reused by other tools such as:

    - analyze_stock()
    - create_price_chart()
    - create_volume_chart()
    - compare_stocks()
    - calculate_indicators()
    - analyze_portfolio()

    By caching downloaded data, repeated API requests are avoided, making
    subsequent analyses significantly faster.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g. "AAPL", "TSLA", "MSFT").

    period : str, optional
        Historical period to download.
        Examples:
        "1d", "5d", "1mo", "3mo", "6mo",
        "1y", "2y", "5y", "10y", "max".

    interval : str, optional
        Data interval.
        Examples:
        "1m", "2m", "5m", "15m",
        "30m", "1h", "1d", "1wk", "1mo".

    Returns
    -------
    dict
        Dictionary containing metadata about the downloaded dataset.

        Example:

        {
            "symbol": "AAPL",
            "period": "1y",
            "interval": "1d",
            "rows": 252,
            "start_date": "2025-07-01",
            "end_date": "2026-06-30",
            "csv_path": "stock_data/AAPL_1y_1d.csv"
        }
    """

    df, csv_path = load_stock_data(symbol, period, interval)

    return {
        "symbol": symbol,
        "period": period,
        "interval": interval,
        "rows": len(df),
        "start_date": str(df.index.min().date()),
        "end_date": str(df.index.max().date()),
        "csv_path": str(csv_path),
    }


@mcp.tool()
def analyze_stock(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
    ) -> dict:
    """
    Perform standard financial analysis on a stock.

    PURPOSE
    -------
    Compute commonly used financial statistics directly on the server.

    This avoids unnecessary Python code generation for routine analysis.

    This tool automatically reuses locally cached stock data whenever
    available.

    WHEN TO USE
    -----------

    Use for questions like

    • Analyze Apple stock
    • How did Tesla perform?
    • Highest price
    • Lowest price
    • Percentage gain
    • Average volume
    • Volatility
    • Basic financial summary

    WHEN NOT TO USE
    ---------------

    If raw historical data or custom indicators are required,
    use get_stock_data().

    Returns
    -------

    Dictionary containing

    • symbol
    • start_date
    • end_date
    • first_close
    • last_close
    • pct_change
    • period_high
    • period_low
    • average_volume
    • volatility
    • standard deviation
    • mean close
    • recent OHLCV records

    This tool should be preferred over custom Python whenever possible.
    """

    df, _ = load_stock_data(symbol,period,interval)
    return analyze_dataframe(symbol,df)




@mcp.tool()
def analyze_correlation(
    symbols: list,
    period: str = "1y",
    interval: str = "1d"
) -> dict:
    """
    Analyze correlation between multiple stocks.

    The tool downloads historical closing prices,
    computes the Pearson correlation matrix,
    and returns the result.

    Useful when users ask:

    - Which stocks move together?
    - Correlation between Apple and Microsoft
    - Diversification analysis

    Returns:
        Correlation matrix.
    """

    data = {}
    for symbol in symbols:
        df, _ = load_stock_data(symbol, period, interval)
        data[symbol] = df
    return correlation_analysis(data)



#chart
@mcp.tool()
def generate_chart(
    chart_type: str,
    symbols: list[str],
    period: str = "1y",
    interval: str = "1d",
):
    """
    Generate one financial chart.

    Supported chart types:

    - price
    - volume
    - moving_average
    - candlestick
    - comparison
    - heatmap
    - returns
    - volatility
    - drawdown
    - rsi
    - macd

    Parameters
    ----------
    chart_type:
        Type of chart to generate.

    symbols:
        One or more stock symbols.
    
    period:
        Historical period.

    interval:
        Data interval.

    Returns
    -------
    Path of the generated chart image.
    """   
        

    data = {}

    for symbol in symbols:
        df, _ = load_stock_data(symbol, period, interval)
        data[symbol] = df
    if chart_type == "price":
        return generate_price_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "volume":
        return generate_volume_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "moving_average":
        return generate_ma_chart(
            data[symbols[0]],
            symbols[0]
    )

    elif chart_type == "candlestick":
        return generate_candlestick_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "comparison":
        return generate_comparison_chart(data)

    elif chart_type == "heatmap":
        return generate_heatmap(data)

    elif chart_type == "returns":
        return generate_returns_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "volatility":
        return generate_volatility_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "drawdown":
        return generate_drawdown_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "rsi":
        return generate_rsi_chart(
            data[symbols[0]],
            symbols[0]
        )

    elif chart_type == "macd":
        return generate_macd_chart(
            data[symbols[0]],
            symbols[0]
        )

    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")


@mcp.tool()
def summarize_stock(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
) -> dict:
    """
    Generate an executive summary of the stock.

    Includes:

    - Highest price
    - Lowest price
    - Percentage return
    - Average volume
    - Volatility
    - Trading days
    - Date range

    Returns:
        Summary dictionary.
    """

    df, _ = load_stock_data(symbol, period, interval)
    return create_stock_summary(df, symbol)

@mcp.tool()
def calculate_indicators(
    symbol: str,
    period: str = "1y",
    interval: str = "1d",
):
    """
    Calculate commonly used technical indicators for a stock.

    This tool retrieves historical stock data using the local cache
    (or downloads it if unavailable) and computes several widely used
    technical indicators.

    Indicators include:

    - Current Price
    - SMA 20
    - SMA 50
    - EMA 20
    - RSI (14)
    - MACD
    - MACD Signal
    - MACD Histogram
    - Bollinger Bands

    This tool is intended for financial analysis and should be used
    whenever the user asks about market momentum, trend strength,
    overbought/oversold conditions, or technical trading signals.

    Parameters
    ----------
    symbol : str
        Stock ticker.

    period : str
        Historical period.

    interval : str
        Data interval.

    Returns
    -------
    dict
        Latest values of all calculated indicators.
    """

    df, _ = load_stock_data(symbol, period, interval)

    return calculate_indicators_dataframe(symbol, df)



@mcp.tool()
def generate_pdf_report(
    title: str,
    report: str,
    charts: list[str],
    filename: str = "financial_report.pdf",
):
    """
    Generate a professional PDF financial report.

    Parameters
    ----------
    title:
        Report title.

    report:
        Financial analysis generated by the analyst.

    charts:
        List of chart image paths.

    filename:
        Name of the PDF.

    Returns
    -------
    Dictionary containing:

    - status
    - pdf_path
    - charts_added
    """
    return generate_pdf(
        title=title,
        report=report,
        charts=charts,
        filename=filename,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")