import pandas as pd
import requests
from sqlalchemy import create_engine
from datetime import datetime

# API Dados
def get_ethereum_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "ETHUSDT",  
        "interval": "1d",     
        "limit": 365     
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", 
            "taker_buy_quote_asset_volume", "ignore"
        ])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        return df
    else:
        print(f"Erro: {response.status_code}")
        return None

# Banco de Dados
def save_to_db(df):
    engine = create_engine('postgresql://cecigonca:cecilia2016@localhost:5432/cripto_db')
    df.to_sql('dados_ethereum', engine, schema='public', if_exists='append', index=False, method='multi')

if __name__ == '__main__':
    df = get_ethereum_data()
    if df is not None:
        save_to_db(df)
        print("Dados no banco de dados")
    else:
        print("Deu errado")
