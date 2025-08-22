
# 📊 Crypto Market Analysis & Dashboard (Power BI + Python + MySQL)

## 🚀 Project Overview
This project is an end-to-end **Cryptocurrency Market Analysis Platform** that fetches real-time data from the **CoinMarketCap API**, stores it in a **MySQL database**, performs **Exploratory Data Analysis (EDA) in Python**, and visualizes insights through a **Power BI Dashboard**.

The pipeline is automated to update daily, ensuring fresh data is available for analysis and reporting.

---

## 📂 Project Workflow
1. **Data Collection** – Fetch crypto market data from CoinMarketCap API (Prices, Market Cap, Volume).  
2. **Database Storage** – Store data in MySQL tables (`cryptodata_final`, `marketcap_data`).  
3. **Automation** – Python script scheduled to run daily (via Task Scheduler/CRON).  
4. **EDA & Visualization** – Use Python (pandas, matplotlib, seaborn) for cleaning & analysis.  
5. **Dashboard** – Power BI for interactive visualizations (KPIs, trends, history).  

---

## 🔑 Features
- Automated data collection from CoinMarketCap API.
- MySQL database integration with separate tables for **prices** and **market cap**.
- EDA in Python (distribution plots, correlation heatmaps, moving averages).
- Power BI Dashboard with three main sections:
  - **Home Page** → Global KPIs (Total Market Cap, Bitcoin Price, Total Coins).  
  - **Coins Page** → Comparative analysis of coins (Price, Market Cap, Volume).  
  - **History Page** → Historical average prices, volumes, and BTC daily data.  
- Daily data refresh ensures up-to-date reporting.  

---

## 🛠️ Tools & Technologies
- **Python** (requests, pandas, matplotlib, seaborn, pymysql)
- **MySQL** (Database storage)
- **Power BI** (Dashboard & DAX measures)
- **CoinMarketCap API** (Data source)

---

## 📥 Data Collection (CoinMarketCap API)

### Python Script (Data Fetching & Storage)
```python
import requests
import pymysql as sql
from datetime import datetime

# API Setup
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
```

## Market Captial Featching using API

### Python :

```python
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

````


## 🗄️ MySQL Database Setup

### Create Database

```sql
CREATE DATABASE crypto;
USE crypto;
```

### Create Tables

```sql
-- Table 1: Price Data
CREATE TABLE crypto_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(50),
    date DATETIME,
    price DECIMAL(18,2),
    total_volume FLOAT(20,5)
);

-- Table 2: Market Cap Data
CREATE TABLE market_value(
name VARCHAR(244),
date datetime,
market_cap float(20,3));
```
---

## ⚙️ Automation

* The Python script is scheduled to run **daily** using **Task Scheduler (Windows)** or **CRON (Linux)**.
* Each run appends fresh values into MySQL tables, ensuring continuous updates.

---

## 📊 Exploratory Data Analysis (EDA)

Python was used for EDA before connecting data to Power BI. Key steps:

* **Data Cleaning** → Removed null values, formatted dates, ensured numeric precision.
* **Descriptive Stats** → Mean, Median, Max, Min of prices & volumes.
* **Visualizations**:

  * Price distribution of top coins
  * Correlation heatmap between prices & volumes
  * Rolling average price trends (7-day, 30-day)

Example EDA Code:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_sql("SELECT * FROM crypto_price", db)

# Correlation heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Between Crypto Metrics")
plt.show()
```
---
For making the analysis simple I have also created a .csv file of the date uptill the date I am creating this repo.

**All The analysis of the data is added to the EDA Crypto Data/Insights**

![Bitcoin Trading Volume](EDA%20Crypto%20Data/Insights/Bitcoin%20Trading%20Volume%20Over%20Time.png)

## 📈 Power BI Dashboard

### Pages

1. **Home Page** – KPIs, Market Cap of Top 6 Coins, Most Traded Coins.
2. **Coins Page** – Average Price, Market Cap, Comparative visuals.
3. **History Page** – Average Price by Year, Historical Volume by Period, Daily BTC Price Table.

### Key DAX Measures

* Latest Bitcoin Price

```DAX
Latest BTC Price = 
CALCULATE(
    LASTNONBLANKVALUE(cryptodata_final[date], SUM(cryptodata_final[price])),
    cryptodata_final[symbol] = "BTC"
)
```

* Total Market Cap

```DAX
Total Market Cap = SUM(marketcap_data[market_cap])
```

---

## 📂 File Structure

```
crypto-dashboard/
│
├── data/
│   ├── raw_data.csv
│   ├── processed_data.csv
│
├── scripts/
│   ├── fetch_data.py
│   ├── eda_visuals.py
│
├── dashboard/
│   ├── crypto_dashboard.pbix
│   ├── final_dashboard.pdf
│
├── README.md
├── LICENSE
```

---

## 📜 License

This project is licensed under the **MIT License** – you are free to use, modify, and distribute with attribution.

---

## 🙌 Contributors

* **Your Name** – Developer & Analyst

---

```

---

✅ This README is **comprehensive** — it covers **data fetching, MySQL schema, automation, EDA, Power BI, file structure, and license**.   
---
