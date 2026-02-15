select * from gold_prices_usd

CREATE TABLE gold_prices_usd (
    price_date DATE PRIMARY KEY,
    usd_spot_oz DECIMAL(10,2),
    usd_goldbod_oz DECIMAL(10,2),
    usd_goldbod_lb DECIMAL(10,2),
    source VARCHAR(20),
    is_flagged BIT,
    load_time DATETIME2 DEFAULT SYSUTCDATETIME()
);

drop table gold_prices_usd

create database CommoditiesDB