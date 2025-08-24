import yfinance as yf
import pymysql as sql
from datetime import datetime

# MySQL Connection
def Connection():
    return sql.connect(
        host='localhost',
        user='root',
        password='p12345',
        database='crypto',
        port=3306
    )

# Your specific list of coins in Yahoo Finance format
symbols = [
    "ADA-USD","AVAX-USD","BCH-USD","BNB-USD","BTC-USD","DOGE-USD","ETH-USD",
    "HBAR-USD","HYPE-USD","LEO-USD","LINK-USD","LTC-USD","SOL-USD","SUI-USD",
    "TON-USD","TRX-USD","USDC-USD","USDE-USD","USDT-USD","XLM-USD","XRP-USD"
]

for symbol in symbols:
    try:
        # Fetch today's data with exact OHLCV
        data = yf.download(symbol, period="1d", interval="1d", auto_adjust=False)
        if data.empty:
            print(f"⚠ No data for {symbol}, skipping.")
            continue

        row = data.iloc[-1]
        date = row.name.strftime("%Y-%m-%d")
        open_price = float(row['Open'])
        high = float(row['High'])
        low = float(row['Low'])
        close = float(row['Close'])
        volume = float(row['Volume'])

        # Clean symbol (remove -USD)
        clean_symbol = symbol.replace("-USD", "")

        conn = Connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO ohlc(date, symbol, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            open = VALUES(open),
            high = VALUES(high),
            low = VALUES(low),
            close = VALUES(close),
            volume = VALUES(volume)
        """
        values = (date, clean_symbol, open_price, high, low, close, volume)

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        print(f"{clean_symbol} inserted/updated for {date}")

    except Exception as e:
        print(f"❌ Error fetching/storing {symbol}: {e}")
