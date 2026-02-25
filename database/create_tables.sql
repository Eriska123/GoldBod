CREATE DATABASE CommoditiesDB;
USE CommoditiesDB;


CREATE TABLE [dbo].[gold_prices_usd](
	[price_date] [date] NOT NULL,
	[usd_spot_oz] [decimal](10, 2) NULL,
	[usd_goldbod_oz] [decimal](10, 2) NULL,
	[usd_goldbod_lb] [decimal](10, 2) NULL,
	[source] [varchar](20) NULL,
	[is_flagged] [bit] NULL,
	[load_time] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[price_date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]