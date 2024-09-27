import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar dados
def carregar_dados():
    df_ethereum = pd.read_csv('./df_ethereum_processado.csv')
    df_ethereum['timestamp'] = pd.to_datetime(df_ethereum['timestamp'])
    return df_ethereum

# Função para criar gráficos exploratórios
def grafico_exploratorio(df_ethereum):
    st.subheader("Gráfico Histórico de Preços de Fechamento (Exploratório)")
    plt.figure(figsize=(10, 6))
    plt.plot(df_ethereum['timestamp'], df_ethereum['close'], label='Fechamento', color='blue')
    plt.title('Histórico de Preços de Fechamento')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

# Função para rodar os modelos e gerar previsões
def executar_modelos(df_ethereum):
    # Simulação de previsões dos modelos
    forecast_arima = np.random.random(7)  # Previsão ARIMA simulada
    forecast_hw = np.random.random(7)     # Previsão Holt-Winters simulada
    pred_rf = np.random.choice([0, 1], size=7)  # Previsão Random Forest simulada

    # Simulando datas futuras para as previsões
    last_date = df_ethereum['timestamp'].iloc[-1]
    future_dates = pd.date_range(start=last_date, periods=7)

    # Criar DataFrame com as previsões dos modelos
    previsoes = pd.DataFrame({
        'Data': future_dates,
        'Previsão ARIMA': forecast_arima,
        'Previsão Holt-Winters': forecast_hw,
        'Previsão Random Forest': pred_rf
    })

    # Exibir as previsões em formato de tabela
    st.subheader("Resultados das Previsões")
    st.table(previsoes)

# Interface do Streamlit
st.title('Dashboard de Previsão de Criptoativos')

# Carregar dados
df_ethereum = carregar_dados()

# Exibir gráficos exploratórios assim que a aplicação é carregada
grafico_exploratorio(df_ethereum)

# Botão para executar previsões
if st.button('Executar Previsões'):
    executar_modelos(df_ethereum)
