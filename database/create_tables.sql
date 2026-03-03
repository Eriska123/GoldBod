CREATE DATABASE CommoditiesDB;
USE CommoditiesDB;
-- Create database only if it doesn't exist
IF NOT EXISTS (
    SELECT name FROM sys.databases WHERE name = 'CommoditiesDB'
)
BEGIN
    CREATE DATABASE CommoditiesDB;
END
GO

-- Switch to database
USE CommoditiesDB;
GO

-- Create table only if it doesn't exist
IF NOT EXISTS (
    SELECT * FROM sys.tables WHERE name = 'gold_prices_usd'
)
BEGIN
    CREATE TABLE dbo.gold_prices_usd (
        price_date DATE PRIMARY KEY,
        usd_spot_oz FLOAT NOT NULL,
        usd_goldbod_oz FLOAT NOT NULL,
        usd_goldbod_lb FLOAT NOT NULL,
        source NVARCHAR(50) NOT NULL,
        is_flagged BIT NOT NULL
    );
END
GO