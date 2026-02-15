import streamlit as st
import pandas as pd
import pyodbc
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GoldBod Gold Price Dashboard",
    layout="wide"
)

st.title("📊 GoldBod Gold Price Dashboard (USD)")
st.caption("Source: GLD proxy • GoldBod-adjusted pricing")

# =====================================================
# DATABASE CONFIG
# =====================================================

SERVER = r"DESKTOP-F3EJ92V\SQLEXPRESS"
DATABASE = "CommoditiesDB"
TABLE = "gold_prices_usd"

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(ttl=300)
def load_data():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
    )

    df = pd.read_sql(f"""
        SELECT
            price_date,
            usd_spot_oz,
            usd_goldbod_oz,
            is_flagged
        FROM {TABLE}
        ORDER BY price_date
    """, conn)

    conn.close()

    df["price_date"] = pd.to_datetime(df["price_date"])
    return df

df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# =====================================================
# DATE FILTER SLIDER (NEW)
# =====================================================

min_date = df["price_date"].min().date()
max_date = df["price_date"].max().date()

start_date, end_date = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

df = df[
    (df["price_date"].dt.date >= start_date) &
    (df["price_date"].dt.date <= end_date)
]

# =====================================================
# METRICS CALCULATION
# =====================================================

df = df.sort_values("price_date")

df["3od_ma"] = df["usd_goldbod_oz"].rolling(3).mean()
df["daily_return"] = df["usd_goldbod_oz"].pct_change()
df["volatility_3od"] = df["daily_return"].rolling(3).std() * np.sqrt(3)

# YoY % Change
latest_price = df["usd_goldbod_oz"].iloc[-1]

one_year_ago = df[
    df["price_date"] <= df["price_date"].max() - pd.DateOffset(years=1)
]

if not one_year_ago.empty:
    yoy_price = one_year_ago.iloc[-1]["usd_goldbod_oz"]
    yoy_change = ((latest_price - yoy_price) / yoy_price) * 100
else:
    yoy_change = np.nan

# =====================================================
# KPI DISPLAY
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Avg Gold Spot Price (USD/oz)", f"${df['usd_spot_oz'].mean():,.2f}")
col2.metric("Avg GoldBod Price (USD/oz)", f"${df['usd_goldbod_oz'].mean():,.2f}")
col3.metric("YoY % Change", f"{yoy_change:.2f}%" if not np.isnan(yoy_change) else "N/A")
col4.metric("3OD Moving Avg (USD/oz)", f"${df['3od_ma'].iloc[-1]:,.2f}")
col5.metric("Volatility (3OD)", f"{df['volatility_3od'].iloc[-1]:.4f}")

# =====================================================
# PRICE TREND CHART
# =====================================================

st.subheader("📈 Gold Price Trend")

st.line_chart(
    df.set_index("price_date")[["usd_spot_oz", "usd_goldbod_oz", "3od_ma"]]
)

# =====================================================
# YOY TREND CHART (NEW)
# =====================================================

st.subheader("📉 Year-on-Year % Change Trend")

df["yoy_pct"] = (
    df["usd_goldbod_oz"]
    .pct_change(periods=252) * 100
)

st.line_chart(
    df.set_index("price_date")[["yoy_pct"]]
)

# =====================================================
# VOLATILITY CHART
# =====================================================

st.subheader("📊 Volatility (3OD)")

st.line_chart(
    df.set_index("price_date")[["volatility_3od"]]
)

# =====================================================
# DATA QUALITY FLAGS
# =====================================================

st.subheader("⚠️ Flagged Observations")

flagged = df[df["is_flagged"] == 1]

if flagged.empty:
    st.success("No anomalies detected.")
else:
    st.dataframe(
        flagged[["price_date", "usd_goldbod_oz"]],
        use_container_width=True
    )
