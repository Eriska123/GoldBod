import yfinance as yf
import pyodbc
import pandas as pd
from datetime import datetime, timedelta, timezone

SERVER = r"DESKTOP-F3EJ92V\SQLEXPRESS"
DATABASE = "CommoditiesDB"
TABLE = "gold_prices_usd"

OUNCES_PER_POUND = 14.5833

# GoldBod policy factors (can be adjusted later)
PURITY_FACTOR = 0.92
POLICY_MARGIN = 1.015

# -----------------------------------
# Database helpers
# -----------------------------------
def get_conn():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
    )

def get_last_loaded_date():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT MAX(price_date) FROM {TABLE}")
    row = cur.fetchone()
    conn.close()
    return row[0]

# -----------------------------------
# Step 1: Incremental fetch
# -----------------------------------
def fetch_gold_history(start_date):
    ticker = yf.Ticker("GLD")  # Most stable proxy
    df = ticker.history(
        start=start_date,
        end=datetime.now(timezone.utc).date() + timedelta(days=1),
        auto_adjust=False
    )

    if df.empty:
        raise RuntimeError("No gold data returned")

    df = df[["Close"]].dropna()
    df.rename(columns={"Close": "usd_spot_oz"}, inplace=True)

    # GLD ≈ 1/10 oz
    df["usd_spot_oz"] *= 10

    df.reset_index(inplace=True)
    df["Date"] = df["Date"].dt.date

    return df

# -----------------------------------
# Step 2: Validation & outlier detection
# -----------------------------------
def validate_prices(df):
    df["pct_change"] = df["usd_spot_oz"].pct_change()
    df["is_flagged"] = (
        (df["usd_spot_oz"] <= 0) |
        (df["pct_change"].abs() > 0.10)
    )
    return df

# -----------------------------------
# Step 3: GoldBod pricing layer
# -----------------------------------
def apply_goldbod_pricing(df):
    df["usd_goldbod_oz"] = (
        df["usd_spot_oz"] * PURITY_FACTOR * POLICY_MARGIN
    ).round(2)

    df["usd_goldbod_lb"] = (
        df["usd_goldbod_oz"] * OUNCES_PER_POUND
    ).round(2)

    return df

# -----------------------------------
# Persist incrementally
# -----------------------------------
def store_incremental(df):
    conn = get_conn()
    cur = conn.cursor()

    for _, r in df.iterrows():
        cur.execute(f"""
            IF NOT EXISTS (
                SELECT 1 FROM {TABLE} WHERE price_date = ?
            )
            INSERT INTO {TABLE}
            (price_date, usd_spot_oz, usd_goldbod_oz, usd_goldbod_lb, source, is_flagged)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        r["Date"], r["Date"], r["usd_spot_oz"],
        r["usd_goldbod_oz"], r["usd_goldbod_lb"],
        "GLD", int(r["is_flagged"])
        )

    conn.commit()
    conn.close()

# -----------------------------------
# Main execution
# -----------------------------------
if __name__ == "__main__":
    last_date = get_last_loaded_date()

    if last_date is None:
        start_date = datetime(2025, 1, 1).date()
    else:
        start_date = last_date + timedelta(days=1)

    print(f"Loading gold prices from {start_date}")

    df = fetch_gold_history(start_date)
    df = validate_prices(df)
    df = apply_goldbod_pricing(df)
    store_incremental(df)

    print("Gold price pipeline completed successfully.")



