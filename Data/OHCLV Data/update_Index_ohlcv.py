import os
import duckdb
import pandas as pd
import yfinance as yf
from datetime import datetime, date, timedelta
from pathlib import Path

# Find project root automatically
def find_project_root():
    """Find project root by looking for Data or backend folder"""
    curr = Path(__file__).resolve()
    for parent in [curr.parent] + list(curr.parents):
        if (parent / "Data").exists() and (parent / "backend").exists():
            return parent
    raise FileNotFoundError(f"Could not find project root (Data/backend folders) in any parent directory of {curr}")

PROJECT_ROOT = find_project_root()

# Database path
DB_PATH = PROJECT_ROOT / "Data" / "OHCLV Data" / "index.duckdb"

# Configuration
YEARS_BACK = 10
START_DATE = date.today() - timedelta(days=YEARS_BACK * 365)
YESTERDAY = date.today() - timedelta(days=1)

# Indian indices to track
INDICES = [
    "^NSEI",  # Nifty 50
    "^NSEBANK",  # Nifty Bank
    "^NSMIDCP",  # Nifty Midcap 100
    "^CNX500",  # Nifty 500 (may not be available on Yahoo Finance)
]

def normalize(col: str) -> str:
    return col.strip().lower().replace(" ", "_").replace("-", "_")

def get_table_columns(conn):
    rows = conn.execute("PRAGMA table_info('index_ohlcv')").fetchall()
    return [r[1] for r in rows]

def init_db():
    conn = duckdb.connect(str(DB_PATH))
    conn.execute("""
      CREATE TABLE IF NOT EXISTS index_ohlcv (
        symbol VARCHAR,
        date   DATE
      );
    """)
    conn.close()

def insert_dynamic(conn, df: pd.DataFrame):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=normalize)
    df['date'] = pd.to_datetime(df['date'])
    df['symbol'] = df['symbol']
    existing = get_table_columns(conn)
    # Ensure all columns in df are present in table, add if not
    for col in df.columns:
        if col not in existing:
            if col in ('symbol', 'date'):
                continue
            conn.execute(f'ALTER TABLE index_ohlcv ADD COLUMN {col} DOUBLE;')
            existing.append(col)
    for col in existing:
        if col not in df.columns:
            df[col] = None
    to_ins = df[existing]
    conn.register("new_data", to_ins)
    conn.execute(f"INSERT INTO index_ohlcv SELECT * FROM new_data;")
    conn.unregister("new_data")

def fetch_and_insert(symbol):
    fetch_start = START_DATE
    fetch_end = YESTERDAY + timedelta(days=1)
    conn_r = duckdb.connect(str(DB_PATH))
    # Find latest date present in DB for symbol, if any
    last = conn_r.execute("SELECT MAX(date) FROM index_ohlcv WHERE symbol=?", (symbol,)).fetchone()[0]
    conn_r.close()
    # Only fetch missing dates (after latest date)
    if last:
        last_dt = pd.to_datetime(last).date()
        if last_dt >= YESTERDAY:
            return symbol, 0, None, None, "uptodate"
        fetch_start = max(fetch_start, last_dt + timedelta(days=1))
    if fetch_start > YESTERDAY:
        return symbol, 0, None, None, "uptodate"
    
    try:
        df = yf.Ticker(symbol).history(
            start=fetch_start,
            end=fetch_end,
            auto_adjust=False,
            actions=True
        )
        if df.empty:
            return symbol, 0, None, None, "skipped"
        df = df.reset_index()
        df['symbol'] = symbol
        conn_w = duckdb.connect(str(DB_PATH))
        # For each row, if already present for (symbol, date), check if values match
        for _, row in df.iterrows():
            row_date = pd.to_datetime(row['Date']).date()
            db_row = conn_w.execute(
                "SELECT * FROM index_ohlcv WHERE symbol=? AND date=?",
                (symbol, row_date)
            ).fetchdf()
            # Normalize columns for comparison
            values_are_different = True
            if not db_row.empty:
                db_row_sorted = db_row[df.columns.intersection(db_row.columns)]
                df_row_sorted = pd.DataFrame([row])[db_row.columns.intersection(df.columns)]
                values_are_different = not db_row_sorted.equals(df_row_sorted)
            if values_are_different:
                # Remove any old for that date and insert new
                conn_w.execute("DELETE FROM index_ohlcv WHERE symbol=? AND date=?", (symbol, row_date))
                insert_dynamic(conn_w, pd.DataFrame([row]))
        conn_w.close()
        first_dt = df['Date'].min().date()
        last_dt = df['Date'].max().date()
        return symbol, len(df), first_dt, last_dt, "success"
    except Exception as e:
        return symbol, 0, None, None, f"FAILED: {e}"

def main():
    init_db()
    indices = INDICES
    total = len(indices)
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = failed = skipped = uptodate = 0
    processed = 0
    
    print(f"Updating {total} indices...")
    for idx, symbol in enumerate(indices, start=1):
        percent = idx / total * 100
        try:
            _, count, first_dt, last_dt, status_flag = fetch_and_insert(symbol)
            processed += 1
            if status_flag == "success":
                success += 1
                status = f"+{count} rows ({first_dt}->{last_dt})"
            elif status_flag == "skipped":
                skipped += 1
                status = "skipped"
            elif status_flag == "uptodate":
                uptodate += 1
                status = "up-to-date"
            else:
                status = status_flag
        except Exception as e:
            failed += 1
            status = f"FAILED: {e}"
        print(f"{idx}/{total} ({percent:.1f}%): {symbol} -> {status}")
    
    print(f"\n[OK] Index update complete.")
    print(f"Success: {success}, Failed: {failed}, Skipped: {skipped}, Up-to-date: {uptodate}")

if __name__ == "__main__":
    main()
