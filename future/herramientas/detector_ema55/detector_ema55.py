from binance.client import Client
from pybit.unified_trading import HTTP 
import talib
import numpy as np

# Configuración de las claves API
api_key = ""
api_secret = ""

# Inicializar cliente de Binance
client = Client(api_key, api_secret)
bybit_client = HTTP(api_key=api_key, api_secret=api_secret)

def detectar_proximidad_ema(intervalo="1w", umbral=0.01):
    """
    Detecta activos de futuros en Binance cuyo precio actual está cerca de la EMA de 55.
    
    :param intervalo: Temporalidad para los datos (por ejemplo, '15m', '1h').
    :param umbral: Porcentaje de proximidad entre el precio y la EMA (ejemplo: 0.01 = 1%).
    :return: Lista de activos que cumplen con la condición.
    """
    activos = []
    
    # Obtener lista de pares de futuros
    exchange_info = client.futures_exchange_info()
    symbols = [s['symbol'] for s in exchange_info['symbols'] if s['contractType'] == 'PERPETUAL']
    
    for symbol in symbols:
        try:
            # Obtener datos históricos (velas)
            klines = client.futures_klines(symbol=symbol, interval=intervalo, limit=100)
            closes = np.array([float(k[4]) for k in klines])  # Precio de cierre
            
            # Calcular EMA de 55 periodos
            ema_55 = talib.EMA(closes, timeperiod=54)
            
            # Comparar precio actual con la EMA más reciente
            precio_actual = closes[-1]
            diferencia = abs(precio_actual - ema_55[-1])
            
            # Verificar si la diferencia está dentro del umbral
            if diferencia / precio_actual <= umbral:
                activos.append({
                    "symbol": symbol,
                    "precio_actual": precio_actual,
                    "ema_55": ema_55[-1],
                    "diferencia": diferencia
                })
        
        except Exception as e:
            print(f"Error con {symbol}: {e}")
    
    for activo in activos:
        print(f"{activo['symbol']} - Precio: {activo['precio_actual']}, EMA 55: {activo['ema_55']}, Diferencia: {activo['diferencia']}")

def detectar_proximidad_ema_bybit(intervalo="1w", umbral=0.01):
    """
    Detecta activos en Bybit cuyo precio actual está cerca de la EMA de 55.
    """
    activos = []
    symbols_response = bybit_client.get_instruments_info(category="linear")  # Solo futuros lineales (USDT)
    symbols = [s['symbol'] for s in symbols_response['result']['list']]
    
    for symbol in symbols:
        try:
            kline_response = bybit_client.get_kline(category="linear", symbol=symbol, interval=intervalo, limit=100)
            closes = np.array([float(k['close']) for k in kline_response['result']['list']])
            ema_55 = talib.EMA(closes, timeperiod=54)
            print("AQUI")
            precio_actual = closes[-1]
            diferencia = abs(precio_actual - ema_55[-1])
            if diferencia / precio_actual <= umbral:
                activos.append({
                    "exchange": "Bybit",
                    "symbol": symbol,
                    "precio_actual": precio_actual,
                    "ema_55": ema_55[-1],
                    "diferencia": diferencia
                })
        except Exception as e:
            print(f"Error con {symbol} en Bybit: {e}")
    
    for activo in activos:
        print(f"{activo['symbol']} - Precio: {activo['precio_actual']}, EMA 55: {activo['ema_55']}, Diferencia: {activo['diferencia']}")

# Ejemplo de uso
if __name__ == "__main__":
    activos_cercanos = detectar_proximidad_ema(intervalo="5m", umbral=0.036)
    
