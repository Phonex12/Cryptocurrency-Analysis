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
    response.raise_for_status()  

    data = response.json()

    for i in data['data']:
        name = i['name']
        raw_date = i['last_updated']
        date_added = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        market_cap = i['quote']['USD']['market_cap']   # ✅ market cap

        conn = Connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO market_value (name, date, market_cap)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            date = VALUES(date),
            market_cap = VALUES(market_cap)
        """
        values = (name, date_added, market_cap)
        cursor.execute(query, values)
        conn.commit()
        print(f"{name} inserted or updated successfully.")
        conn.close()

# ------------------- Handle HTTP Errors ------------------- #
except requests.exceptions.HTTPError as err:
    status_code = err.response.status_code
    if status_code == 400:
        print("❌ 400 Bad Request")
    elif status_code == 401:
        print("❌ 401 Unauthorized: Check your API key.")
    elif status_code == 403:
        print("❌ 403 Forbidden: Not allowed to access this endpoint.")
    elif status_code == 429:
        print("⏳ 429 Too Many Requests: Waiting 1 min...")
        time.sleep(60)
    else:
        print(f"❌ HTTP Error {status_code}: {err}")

except requests.exceptions.ConnectionError:
    print("❌ Connection Error")
except requests.exceptions.Timeout:
    print("⏰ Timeout Error")
except requests.exceptions.RequestException as e:
    print(f"❌ Request Error: {e}")
except Exception as e:
    print(f"❌ Unknown Error: {e}")
