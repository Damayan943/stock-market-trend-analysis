# Five-Year Stock Market Trend Analysis (2021–2026) | SQL + Power BI

A portfolio project analyzing five years of daily Indian market prices, returns, volatility, trading volume, and relative performance with SQL and Power BI.

> **Data window:** rolling five years ending on the run date (the latest available trading day may be earlier than today). Data is downloaded when you run the Python script; no market data is bundled with this repository.

## Project title for your resume
**Five-Year Stock Market Trend Analysis Using SQL & Power BI**

## What it covers
- Daily OHLC and volume for the NIFTY 50 index and selected NSE-listed stocks.
- SQL tables and views for daily returns, moving averages, monthly performance, and volatility.
- Power BI dashboard design with KPI cards, trend lines, stock comparison, monthly returns, volume analysis, and slicers.
- Reproducible data download and optional SQL Server loading.

## Tickers included
`^NSEI` (NIFTY 50), `RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `HDFCBANK.NS`, `ICICIBANK.NS`, `SBIN.NS`.

## 1. Setup
Install Python 3.10+ and SQL Server (or SQL Server Express). From this folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python python/download_data.py
```

This creates `data/stock_prices.csv` and `data/stock_prices_enriched.csv`. Historical prices are sourced through `yfinance`; check its documentation and Yahoo Finance terms before using the data. See: https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html

## 2. Load into SQL Server
1. Open SQL Server Management Studio (SSMS), connect to your local SQL Server.
2. Run `sql/01_create_database_and_tables.sql`.
3. In SSMS, use **Tasks → Import Data** (or the Import Flat File wizard) to import `data/stock_prices_enriched.csv` into `dbo.StockPrices`. Map columns to the table created by the script. Ensure `TradeDate` is a date and numeric fields are decimal/bigint.
4. Run `sql/02_views_and_analysis.sql`.

Alternatively, set `SQLSERVER_CONNECTION_STRING` and run `python python/load_to_sql.py` after installing the ODBC Driver for SQL Server. Example connection string format is documented in `.env.example`.

## 3. Build the Power BI report
1. Open Power BI Desktop → **Get data → SQL Server**.
2. Enter your server name and database `StockMarketAnalysis`.
3. Import `dbo.StockPrices` and the views in `sql/02_views_and_analysis.sql`.
4. Create a date table (DAX below), mark it as the date table, and relate `DimDate[Date]` to `StockPrices[TradeDate]`.
5. Create the measures in `powerbi/measures.dax`.
6. Suggested report pages:
   - **Market Overview:** latest close, 5-year return, average daily return, annualized volatility, price trend.
   - **Stock Comparison:** indexed performance (base = 100), ticker slicer, return comparison.
   - **Returns & Risk:** monthly return matrix, daily return distribution, rolling volatility.
   - **Volume & Activity:** daily volume trend and volume by ticker.

### Suggested dashboard visuals
- Line chart: `TradeDate` vs `ClosePrice`, legend `Ticker` (use a ticker slicer to avoid clutter).
- Line chart: `TradeDate` vs `MovingAverage50` and `MovingAverage200` (from SQL view).
- Clustered column chart: monthly return by ticker.
- Cards: latest close, cumulative return, annualized volatility, average volume.
- Slicers: ticker, date, year.

## 4. Useful SQL analyses
The SQL scripts include per-ticker daily returns using `LAG`, 50/200-trading-day moving averages, monthly returns, and annualized volatility estimates. Return calculations use adjusted OHLC values because the Python downloader requests adjusted prices; treat these as historical analysis, not investment advice.

## Repository structure
```text
stock_market_trend_analysis/
├── README.md
├── requirements.txt
├── .env.example
├── data/                       # generated CSV files go here
├── python/
│   ├── download_data.py
│   └── load_to_sql.py
├── sql/
│   ├── 01_create_database_and_tables.sql
│   └── 02_views_and_analysis.sql
└── powerbi/
    ├── measures.dax
    └── dashboard_guide.md
```

## Resume description (edit to reflect what you actually complete)
**Five-Year Stock Market Trend Analysis Using SQL & Power BI** — Built a data-analysis workflow for historical NIFTY 50 and selected NSE stocks; used Python to collect and prepare daily market data, SQL window functions to calculate returns and moving averages, and Power BI to design interactive dashboards for trend, performance, volume, and risk analysis.

Only list the project as completed after you have run the pipeline, validated the data, and built the Power BI report.