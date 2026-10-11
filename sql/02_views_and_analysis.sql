USE StockMarketAnalysis;
GO

-- Daily returns and 50/200 trading-day moving averages per ticker.
CREATE OR ALTER VIEW dbo.vw_StockDailyAnalytics AS
WITH base AS (
    SELECT
        TradeDate, Ticker, Company, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume,
        LAG(ClosePrice) OVER (PARTITION BY Ticker ORDER BY TradeDate) AS PreviousClose,
        AVG(ClosePrice) OVER (
            PARTITION BY Ticker ORDER BY TradeDate
            ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
        ) AS MovingAverage50,
        AVG(ClosePrice) OVER (
            PARTITION BY Ticker ORDER BY TradeDate
            ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
        ) AS MovingAverage200
    FROM dbo.StockPrices
)
SELECT *,
    CAST(100.0 * (ClosePrice - PreviousClose) / NULLIF(PreviousClose, 0) AS DECIMAL(12, 4)) AS DailyReturnPct
FROM base;
GO

-- Monthly open-to-close performance and total volume.
CREATE OR ALTER VIEW dbo.vw_MonthlyPerformance AS
WITH month_rows AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY Ticker, YEAR(TradeDate), MONTH(TradeDate) ORDER BY TradeDate ASC) AS rn_first,
        ROW_NUMBER() OVER (PARTITION BY Ticker, YEAR(TradeDate), MONTH(TradeDate) ORDER BY TradeDate DESC) AS rn_last
    FROM dbo.StockPrices
), monthly AS (
    SELECT Ticker, Company, YEAR(TradeDate) AS [Year], MONTH(TradeDate) AS [Month],
        MAX(CASE WHEN rn_first = 1 THEN ClosePrice END) AS FirstClose,
        MAX(CASE WHEN rn_last = 1 THEN ClosePrice END) AS LastClose,
        SUM(Volume) AS MonthlyVolume,
        COUNT(*) AS TradingDays
    FROM month_rows
    GROUP BY Ticker, Company, YEAR(TradeDate), MONTH(TradeDate)
)
SELECT *, CAST(100.0 * (LastClose - FirstClose) / NULLIF(FirstClose, 0) AS DECIMAL(12, 4)) AS MonthlyReturnPct
FROM monthly;
GO

-- Query examples to use in SSMS.
-- 1) Latest available close for each ticker:
-- SELECT p.* FROM dbo.StockPrices p
-- JOIN (SELECT Ticker, MAX(TradeDate) AS MaxDate FROM dbo.StockPrices GROUP BY Ticker) m
--   ON p.Ticker = m.Ticker AND p.TradeDate = m.TradeDate ORDER BY p.Ticker;
-- 2) Best/worst monthly performance:
-- SELECT TOP (10) * FROM dbo.vw_MonthlyPerformance ORDER BY MonthlyReturnPct DESC;
-- SELECT TOP (10) * FROM dbo.vw_MonthlyPerformance ORDER BY MonthlyReturnPct ASC;
-- 3) Annualized volatility (daily return standard deviation * sqrt(252)):
-- SELECT Ticker, STDEV(DailyReturnPct) * SQRT(252.0) AS AnnualizedVolatilityPct
-- FROM dbo.vw_StockDailyAnalytics GROUP BY Ticker ORDER BY AnnualizedVolatilityPct DESC;
GO
