import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Função para buscar dados da API Binance
def get_ethereum_data():
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

        return df
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

# Função para salvar os dados no banco de dados
def save_to_db(df):
    # Conectar ao banco de dados PostgreSQL
    engine = create_engine('postgresql://cecigonca:cecilia2016@localhost:5432/cripto_db')
    
    # Salvando os dados na tabela existente 'dados_ethereum' no esquema 'public'
    df.to_sql('dados_ethereum', engine, schema='public', if_exists='append', index=False, method='multi')

if __name__ == '__main__':
    df = get_ethereum_data()
    if df is not None:
        save_to_db(df)
        print("Dados salvos no banco de dados!")
    else:
        print("Falha ao obter os dados da API.")
