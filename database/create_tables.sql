-- Ensure database exists
IF NOT EXISTS (
    SELECT name FROM sys.databases WHERE name = 'CommoditiesDB'
)
BEGIN
    CREATE DATABASE CommoditiesDB;
END
GO

USE CommoditiesDB;
GO

-- Ensure table exists
IF NOT EXISTS (
    SELECT * FROM sys.tables WHERE name = 'gold_prices_usd'
)
BEGIN
    CREATE TABLE dbo.gold_prices_usd (
        price_date DATE NOT NULL PRIMARY KEY,
        usd_spot_oz DECIMAL(18,4) NOT NULL,
        usd_goldbod_oz DECIMAL(18,2) NOT NULL,
        usd_goldbod_lb DECIMAL(18,2) NOT NULL,
        source NVARCHAR(50) NOT NULL,
        is_flagged BIT NOT NULL
    );
END
GO

