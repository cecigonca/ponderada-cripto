import pandas as pd
import numpy as np
import logging
from keras.models import Sequential
from keras.layers import GRU, Dense
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('postgresql://cecigonca:cecilia2016@localhost:5432/cripto_db')

# Puxa dados do banco de dados
df_ethereum = pd.read_sql('SELECT * FROM public.dados_ethereum_processado', engine)

# Preparo GRU
def create_sequences(data, window_size=60):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X), np.array(y)

# Executando os modelos em sequência
def executar_modelos():

    # MODELO GRU
    def modelo_gru():
        scaler = MinMaxScaler()
        df_ethereum['close'] = scaler.fit_transform(df_ethereum[['close']])
        X, y = create_sequences(df_ethereum['close'].values, 60)
        X_train, X_test = X[:int(0.8 * len(X))], X[int(0.8 * len(X)):]
        y_train, y_test = y[:int(0.8 * len(y))], y[int(0.8 * len(y)):]
        
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        model = Sequential()
        model.add(GRU(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(GRU(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        model.fit(X_train, y_train, epochs=10, batch_size=32)
        y_pred = model.predict(X_test)

        logging.info(f"Previsão GRU: {y_pred.flatten()[-7:].tolist()}")
        return y_pred.flatten()[-7:] # uma semana

    # MODELO ARIMA
    def modelo_arima():
        model = ARIMA(df_ethereum['close'], order=(5, 1, 2))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=30)
        
        logging.info(f"Previsão ARIMA: {forecast[-7:].tolist()}")
        return forecast[-7:]  

    # MODELO HOLT-WINTERS
    def modelo_hwinters():
        model = ExponentialSmoothing(df_ethereum['close'], trend='add', seasonal='add', seasonal_periods=7)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=30)
        
        logging.info(f"Previsão Holt-Winters: {forecast[-7:].tolist()}")
        return forecast[-7:] 

    # MODELO RANDOM FOREST
    def modelo_random_forest():
        df_ethereum['price_direction'] = np.where(df_ethereum['close'].shift(-1) > df_ethereum['close'], 1, 0)
        features = ['golden_cross', 'death_cross', 'volume', 'volatility']
        X = df_ethereum[features]
        y = df_ethereum['price_direction']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)

        y_pred = rf_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        logging.info(f"Previsão Random Forest: {y_pred[-7:].tolist()}, Acurácia: {accuracy}")
        return {'accuracy': accuracy, 'predictions': y_pred[-7:]}  

    # Roda os modelos
    pred_gru = modelo_gru()
    pred_arima = modelo_arima()
    pred_hwinters = modelo_hwinters()
    rf_result = modelo_random_forest()
    pred_rf = rf_result['predictions']

    # Lógica para recomendação
    total_up_signals = np.mean([np.mean(pred_gru), np.mean(pred_arima), np.mean(pred_hwinters)]) > 0
    rf_up_signals = np.sum(pred_rf == 1) > 3 
    if total_up_signals and rf_up_signals:
        recomendacao = "Semana boa para comprar!"
    else:
        recomendacao = "Melhor não arriscar..."
    logging.info(f"Recomendação final: {recomendacao}")

    return pred_gru, pred_arima, pred_hwinters, pred_rf, recomendacao

# Acessa novo csv anexado
def processar_csv(df_anexado):
    colunas_esperadas = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    for coluna in colunas_esperadas:
        if coluna not in df_anexado.columns:
            raise ValueError(f"Coluna {coluna} faltando no arquivo CSV enviado.")
    global df_ethereum 
    df_ethereum = pd.concat([df_ethereum, df_anexado], ignore_index=True)
    logging.info("Base de dados atualizada com novos dados do CSV.")
