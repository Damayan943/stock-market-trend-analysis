# Power BI dashboard build guide

## Data model
- Import `dbo.StockPrices` and `dbo.vw_StockDailyAnalytics` plus `dbo.vw_MonthlyPerformance` from SQL Server.
- Create `DimDate = CALENDAR(MIN(StockPrices[TradeDate]), MAX(StockPrices[TradeDate]))`.
- Add `Year = YEAR(DimDate[Date])`, `Month = FORMAT(DimDate[Date], "MMM")`, and `YearMonth = FORMAT(DimDate[Date], "YYYY-MM")` to DimDate.
- Mark DimDate as the date table and relate `DimDate[Date]` → `StockPrices[TradeDate]` (one-to-many).
- If you import SQL views, check relationships and avoid duplicate measures/columns.

## Page 1 — Market Overview
- KPI cards: Latest Close, Five Year / Selected Period Return %, Annualized Volatility %, Total Trading Volume.
- Line chart: Date on X axis, ClosePrice on Y axis, Ticker as legend. Use a ticker slicer to focus on one or two assets.
- Line chart: ClosePrice, MovingAverage50, MovingAverage200 over time (from `vw_StockDailyAnalytics`).

## Page 2 — Stock Comparison
- Line chart with a normalized performance index. For each ticker, normalize its close to 100 at the first selected date; implement as a measure or calculate in Power Query.
- Bar chart: return by ticker.
- Slicers: Ticker, Year, date range.

## Page 3 — Returns & Risk
- Matrix: Year and Month rows, Ticker columns, MonthlyReturnPct values.
- Bar chart: top/bottom monthly returns.
- Line chart: DailyReturnPct and a rolling 20-trading-day volatility measure.

## Page 4 — Volume & Activity
- Line/area chart: daily Volume by ticker.
- Column chart: monthly total volume by ticker.
- Table: date, ticker, close, daily return, volume.

## Formatting tips
- Format returns as percentage, prices with 2 decimals, and volume using display units (K/M/B).
- Add descriptive titles, data-source note, and a “Historical analysis only — not investment advice” footer.
- Confirm the latest date available in the loaded dataset; market holidays mean the latest row is not necessarily today's date.
