CREATE DATABASE CommoditiesDB;
USE CommoditiesDB;

CREATE TABLE gold_prices_usd (
    price_date DATE PRIMARY KEY,
    usd_spot_oz FLOAT,
    usd_goldbod_oz FLOAT,
    usd_goldbod_lb FLOAT,
    source NVARCHAR(50),
    is_flagged BIT
);