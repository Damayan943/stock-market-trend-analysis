"""Download rolling five-year daily adjusted prices for selected NSE tickers."""
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
TICKERS = {
    "^NSEI": "NIFTY 50",
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank of India",
}
END_DATE = date.today() + timedelta(days=1)  # end is exclusive in yfinance
START_DATE = date.today() - timedelta(days=5 * 365 + 2)


def main() -> None:
    frames = []
    for ticker, company in TICKERS.items():
        print(f"Downloading {ticker} ({company})...")
        hist = yf.download(
            ticker,
            start=START_DATE.isoformat(),
            end=END_DATE.isoformat(),
            interval="1d",
            auto_adjust=True,
            progress=False,
            multi_level_index=False,
            actions=False,
        )
        if hist is None or hist.empty:
            print(f"WARNING: no data returned for {ticker}; skipping.")
            continue
        hist = hist.reset_index()
        date_col = "Date" if "Date" in hist.columns else hist.columns[0]
        hist = hist.rename(columns={
            date_col: "TradeDate", "Open": "OpenPrice", "High": "HighPrice",
            "Low": "LowPrice", "Close": "ClosePrice", "Volume": "Volume"
        })
        hist["Ticker"] = ticker
        hist["Company"] = company
        keep = ["TradeDate", "Ticker", "Company", "OpenPrice", "HighPrice", "LowPrice", "ClosePrice", "Volume"]
        hist = hist[keep]
        hist["TradeDate"] = pd.to_datetime(hist["TradeDate"]).dt.date
        for col in ["OpenPrice", "HighPrice", "LowPrice", "ClosePrice"]:
            hist[col] = pd.to_numeric(hist[col], errors="coerce")
        hist["Volume"] = pd.to_numeric(hist["Volume"], errors="coerce").fillna(0).astype("int64")
        hist = hist.dropna(subset=["TradeDate", "ClosePrice"])
        frames.append(hist)

    if not frames:
        raise RuntimeError("No market data was downloaded. Check connectivity and ticker symbols.")

    prices = pd.concat(frames, ignore_index=True).sort_values(["Ticker", "TradeDate"])
    prices["DailyReturnPct"] = prices.groupby("Ticker")["ClosePrice"].pct_change() * 100
    prices["MovingAverage50"] = prices.groupby("Ticker")["ClosePrice"].transform(lambda s: s.rolling(50, min_periods=1).mean())
    prices["MovingAverage200"] = prices.groupby("Ticker")["ClosePrice"].transform(lambda s: s.rolling(200, min_periods=1).mean())
    prices["Year"] = pd.to_datetime(prices["TradeDate"]).dt.year
    prices["Month"] = pd.to_datetime(prices["TradeDate"]).dt.month
    prices["YearMonth"] = pd.to_datetime(prices["TradeDate"]).dt.strftime("%Y-%m")

    raw_path = DATA_DIR / "stock_prices.csv"
    enriched_path = DATA_DIR / "stock_prices_enriched.csv"
    prices[["TradeDate", "Ticker", "Company", "OpenPrice", "HighPrice", "LowPrice", "ClosePrice", "Volume"]].to_csv(raw_path, index=False)
    prices.to_csv(enriched_path, index=False)
    print(f"Saved {len(prices):,} rows to {raw_path}")
    print(f"Saved enriched dataset to {enriched_path}")
    print("Data window:", prices["TradeDate"].min(), "to", prices["TradeDate"].max())


if __name__ == "__main__":
    main()
