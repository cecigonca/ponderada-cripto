import requests
import pandas as pd
from datetime import datetime

# Definir a URL da API Binance
url = "https://api.binance.com/api/v3/klines"

# Definir os parâmetros da API
params = {
    "symbol": "ETHUSDT",  # Par de negociação Ethereum/USDT
    "interval": "1d",     # Intervalo de tempo de 1 dia
    "limit": 365          # Número de dados (últimos 365 dias)
}

# Fazer a requisição GET à API Binance
response = requests.get(url, params=params)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converter a resposta JSON para uma lista de dados
    data = response.json()
    
    # Transformar os dados em um DataFrame do pandas
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", 
        "taker_buy_quote_asset_volume", "ignore"
    ])
    
    # Converter a coluna de timestamp para formato legível
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    
    # Manter apenas as colunas relevantes
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    
    # Converter colunas numéricas para float
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    
    # Exibir as primeiras linhas do DataFrame
    print(df.head())
    
    # Salvar os dados em um arquivo CSV
    df.to_csv("ethereum_365days.csv", index=False)
    print("Dados salvos no arquivo 'ethereum_365days.csv'.")
else:
    print(f"Erro na requisição: {response.status_code}")