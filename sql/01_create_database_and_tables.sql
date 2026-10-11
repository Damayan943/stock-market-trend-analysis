IF DB_ID(N'StockMarketAnalysis') IS NULL
    CREATE DATABASE StockMarketAnalysis;
GO
USE StockMarketAnalysis;
GO

IF OBJECT_ID(N'dbo.StockPrices', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.StockPrices (
        TradeDate DATE NOT NULL,
        Ticker VARCHAR(20) NOT NULL,
        Company NVARCHAR(100) NOT NULL,
        OpenPrice DECIMAL(19, 4) NULL,
        HighPrice DECIMAL(19, 4) NULL,
        LowPrice DECIMAL(19, 4) NULL,
        ClosePrice DECIMAL(19, 4) NOT NULL,
        Volume BIGINT NOT NULL,
        CONSTRAINT PK_StockPrices PRIMARY KEY (TradeDate, Ticker)
    );
END;
GO

CREATE INDEX IX_StockPrices_Ticker_Date ON dbo.StockPrices(Ticker, TradeDate) INCLUDE (ClosePrice, Volume);
GO
