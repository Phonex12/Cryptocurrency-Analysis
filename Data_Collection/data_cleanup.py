import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
import numpy as np

df = pd.read_csv('D:\\Crypto\\Data\\Toncoin Historical Data.csv')
name = input("Enter the name of coin :")
symbol = input("Enter the symbol :")
symbol = symbol.upper()

df['Name'] = name
df['symbol'] = symbol

df['Date'] = pd.to_datetime(df['Date'],format='%d-%m-%Y')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')


# Handle missing or '-' values before evaluating
df['Vol.'] = (
    df['Vol.'].replace('-', np.nan)  # replace '-' with NaN
             .str.upper()  # uppercase
             .replace({'K': '*1000', 'M': '*1000000', 'B': '*1000000000'}, regex=True)
             .apply(lambda x: pd.eval(x, local_dict={'nan': np.nan}) if pd.notna(x) else np.nan)
)


df['Price'] = df['Price'].replace(',', '',regex = True)

# Convert to float
df['Price'] = df['Price'].astype(float)
df['Price'] = df["Price"].astype(float)

df['total_volume'] = df['Vol.'] * df['Price']

df = df[['symbol','Name','Date','Price','total_volume']]

df.rename(columns = {'Name':'name'},inplace=True)
df.rename(columns = {'Date':'date'},inplace=True)
df.rename(columns = {'Price':'price'},inplace=True)

print(df)

my_conn = create_engine('mysql+pymysql://root:p12345@localhost:3306/crypto')
df.to_sql(con = my_conn,name = 'crypto_prices',if_exists="append",index = False)
print("Data inserted Successfully")