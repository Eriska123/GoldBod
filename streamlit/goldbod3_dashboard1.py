import streamlit as st
import pyodbc
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# =====================================================
# Streamlit Page Config
# =====================================================
st.set_page_config(
    page_title="GoldBod Gold Price Dashboard",
    layout="wide"
)
st.title("📊 GoldBod Gold Price Dashboard (USD)")
st.caption("Source: GLD proxy • GoldBod-adjusted pricing")

# =====================================================
# Load Environment Configuration
# =====================================================
load_dotenv("config/.env")

SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
TABLE = "gold_prices_usd"

if not SERVER or not DATABASE:
    st.error("Database configuration missing. Check config/.env")
    st.stop()

# =====================================================
# Connect to Database
# =====================================================
try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
    )
except Exception as e:
    st.error(f"Failed to connect to SQL Server: {e}")
    st.stop()

# =====================================================
# Load Gold Prices
# =====================================================
try:
    df = pd.read_sql(f"SELECT * FROM dbo.{TABLE} ORDER BY price_date", conn)
    conn.close()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# =====================================================
# Defensive Checks
# =====================================================
if df.empty:
    st.warning("No gold price data available yet. Please run the ingestion pipeline first.")
    st.stop()

# Ensure price_date is datetime
df["price_date"] = pd.to_datetime(df["price_date"])

# Check required columns
required_columns = ["price_date", "usd_spot_oz", "usd_goldbod_oz", "usd_goldbod_lb", "is_flagged"]
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    st.error(f"Missing required columns in database: {missing_cols}")
    st.stop()

# =====================================================
# Dashboard Controls
# =====================================================
min_date = df["price_date"].min().date()
max_date = df["price_date"].max().date()

selected_date = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

filtered_df = df[(df["price_date"] >= pd.to_datetime(selected_date[0])) &
                 (df["price_date"] <= pd.to_datetime(selected_date[1]))]

# =====================================================
# Dashboard Visualizations
# =====================================================
st.subheader("GoldBod Pricing Table")
st.dataframe(filtered_df)

st.subheader("GoldBod Prices Over Time")
st.line_chart(filtered_df.set_index("price_date")[["usd_goldbod_oz", "usd_goldbod_lb"]])

st.subheader("Spot Price vs GoldBod Price")
st.line_chart(filtered_df.set_index("price_date")[["usd_spot_oz", "usd_goldbod_oz"]])