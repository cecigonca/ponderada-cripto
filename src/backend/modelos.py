import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Exemplo: Carregar os dados para treinamento
df_ethereum = pd.read_csv('./df_ethereum_processado.csv')

# MODELO GRU
def create_sequences(data, window_size=60):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X), np.array(y)

def modelo_gru():
    scaler = MinMaxScaler()
    df_ethereum['close'] = scaler.fit_transform(df_ethereum[['close']])
    
    X, y = create_sequences(df_ethereum['close'].values, 60)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    model = Sequential()
    model.add(GRU(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(GRU(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    y_pred = model.predict(X_test)

    return y_pred

# MODELO ARIMA
def modelo_arima():
    model = ARIMA(df_ethereum['close'], order=(5, 1, 2))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=30)
    return forecast

# MODELO HOLT-WINTERS
def holt_winters_model():
    model = ExponentialSmoothing(df_ethereum['close'], trend='add', seasonal='add', seasonal_periods=7)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=30)
    return forecast

# VISUALIZAÇÃO ARIMA E HW
def grafico_arima_hw(df, forecast_arima, forecast_hw, num_last_days=30):
    
    # GRÁFICO COMPLETO
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plt.plot(df['timestamp'], df['close'], label='Observado', color='blue', linewidth=2)
    
    last_date = df['timestamp'].iloc[-1]
    future_dates = pd.date_range(start=last_date, periods=len(forecast_arima) + 1)
    
    plt.plot(future_dates[1:], forecast_arima, label='Previsão ARIMA', color='red', linestyle='--', marker='o')
    plt.plot(future_dates[1:], forecast_hw, label='Previsão Holt-Winters', color='green', linestyle='-.', marker='x')
    
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y')) 
    plt.xticks(rotation=45)
    
    plt.title('Comparação de Previsões: ARIMA vs Holt-Winters (Preços Normalizados)', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Preço de Fechamento (Normalizado)', fontsize=12)

    plt.grid(True)
    plt.figure(figsize=(12, 6))
    plt.legend(loc='best', fontsize=12)
    plt.show()

    # GRÁFICO FOCADO
    df_last_days = df.tail(num_last_days)
    plt.plot(df_last_days['timestamp'], df_last_days['close'], label='Passado', color='blue', linewidth=2)
    
    last_date = df_last_days['timestamp'].iloc[-1]
    future_dates = pd.date_range(start=last_date, periods=len(forecast_arima) + 1)
    
    plt.plot(future_dates[1:], forecast_arima, label='Previsão ARIMA', color='red', linestyle='--', marker='o')
    plt.plot(future_dates[1:], forecast_hw, label='Previsão Holt-Winters', color='green', linestyle='-.', marker='x')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1)) 
    plt.gcf().autofmt_xdate()
    
    plt.title(f'Previsões Focadas: ARIMA vs Holt-Winters (Últimos {num_last_days} dias + Previsão)', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Preço de Fechamento (Normalizado)', fontsize=12)
    
    plt.grid()
    plt.figure(figsize=(12, 6))
    plt.legend(loc='best', fontsize=12)
    plt.show()


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

    return {'accuracy': accuracy, 'predictions': y_pred}

def grafico_random_forest():
    plt.figure(figsize=(14, 7))
    plt.plot(df_ethereum['timestamp'][-len(y_test):], y_test, label='Observado', color='blue')
    plt.plot(df_ethereum['timestamp'][-len(y_test):], y_pred, label='Previsão', color='red', linestyle='--')
    plt.title('Previsão de Direção do Preço: Random Forest')
    plt.xlabel('Data')
    plt.ylabel('Direção do Preço (1 = Alta, 0 = Queda)')
    plt.legend()
    plt.grid(True)
    plt.show()