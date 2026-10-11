"""Optional CSV-to-SQL Server loader. Requires SQLSERVER_CONNECTION_STRING in environment."""
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
connection_string = os.getenv("SQLSERVER_CONNECTION_STRING")
if not connection_string:
    raise SystemExit("Set SQLSERVER_CONNECTION_STRING in a .env file. See .env.example")

csv_path = ROOT / "data" / "stock_prices.csv"
if not csv_path.exists():
    raise SystemExit("CSV not found. Run: python python/download_data.py")

df = pd.read_csv(csv_path, parse_dates=["TradeDate"])
engine = create_engine(connection_string, fast_executemany=True)
with engine.begin() as conn:
    conn.execute(text("DELETE FROM dbo.StockPrices"))
df.to_sql("StockPrices", engine, schema="dbo", if_exists="append", index=False, chunksize=1000, method=None)
print(f"Loaded {len(df):,} rows into dbo.StockPrices")
