import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import numpy as np

# === Load CSV ===
df = pd.read_csv(r"C:\Users\Pallav\Downloads\Toncoin Historical Data.csv")

# === Add symbol column ===
symbol = input("Enter the symbol : ").upper()
df['symbol'] = symbol

# === Fix Date Column ===
# Auto-detects format, dayfirst=True ensures 12/8/2025 → 12 Aug 2025
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Convert back to YYYY-MM-DD string (better for SQL)
df = df.dropna(subset=['Date'])
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# === Fix Volume Column ===
def convert_volume(val):
    if pd.isna(val) or val == '-':
        return np.nan
    val = str(val).upper().replace(',', '')
    if val.endswith('K'):
        return float(val[:-1]) * 1_000
    elif val.endswith('M'):
        return float(val[:-1]) * 1_000_000
    elif val.endswith('B'):
        return float(val[:-1]) * 1_000_000_000
    else:
        try:
            return float(val)
        except:
            return np.nan

df['Vol.'] = df['Vol.'].apply(convert_volume)

df.rename(columns = {'Vol.':'volume','Date':'date','Open':'open','High':'high','Low':'low','Price':'close'},inplace = True)
# === Clean Numeric Columns ===
for col in ['open', 'high', 'low', 'close']:
    df[col] = df[col].astype(str).str.replace(',', '', regex=True).astype(float)

# === Final Column Selection ===
df = df[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']]

# print(df.head(10))  # show sample cleaned data

# === Insert into MySQL ===
# Uncomment when ready to push data
my_conn = create_engine('mysql+pymysql://root:p12345@localhost:3306/crypto')
df.to_sql(con=my_conn, name='OHLC', if_exists="append", index=False)
print("Data inserted Successfully")
