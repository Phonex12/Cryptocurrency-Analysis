import requests
import pymysql as sql
import time
from datetime import datetime

# API Setup
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {
    'X-CMC_PRO_API_KEY': '2c250b42-8c52-401e-86aa-408575b8852a',
    'Accept': 'application/json'
}
params = {
    'limit': 20, 
    'sort': 'market_cap',
    'sort_dir': 'desc'
}

# MySQL Connection
def Connection():
    return sql.connect(
        host='localhost',
        user='root',
        password='p12345',
        database='crypto',
        port=3306
    )

# Fetch data with error handling
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises HTTPError for 4xx or 5xx status codes

    data = response.json()

    for i in data['data']:
        symbol = i['symbol']
        name = i['name']
        raw_date = i['last_updated']
        date_added = datetime.strptime(raw_date,"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        price = i['quote']['USD']['price']
        volume = i['quote']['USD']['volume_24h']

        conn = Connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO crypto_prices (symbol, name, date, price, total_volume)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            symbol = VALUES(symbol),
            name = VALUES(name),
            date = VALUES(date),
            price = VALUES(price),
            total_volume = VALUES(total_volume)
        """

        values = (symbol, name, date_added, price, volume)

        cursor.execute(query, values)
        conn.commit()
        print(f"{name} inserted or updated successfully.")
        conn.close()

# ------------------- Handle HTTP Errors ------------------- #
except requests.exceptions.HTTPError as err:
    status_code = err.response.status_code

    if status_code == 400:
        print("❌ 400 Bad Request: The request was unacceptable (maybe a missing parameter).")
    elif status_code == 401:
        print("❌ 401 Unauthorized: Check your API key.")
    elif status_code == 403:
        print("❌ 403 Forbidden: You're not allowed to access this endpoint.")
    elif status_code == 429:
        print("⏳ 429 Too Many Requests: You’ve hit the rate limit. Waiting for 1 minute...")
        time.sleep(60)  # Wait 60 seconds before retrying
        # You can retry the request here if needed
    else:
        print(f"❌ HTTP Error {status_code}: {err}")

# ------------------- Handle Connection or Other Errors ------------------- #
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Check your internet or API URL.")
except requests.exceptions.Timeout:
    print("⏰ Timeout Error: The request took too long.")
except requests.exceptions.RequestException as e:
    print(f"❌ Request Error: {e}")
except Exception as e:
    print(f"❌ Unknown Error: {e}")
