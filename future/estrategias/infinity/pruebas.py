import credenciales
from pybit.unified_trading import HTTP
import json
import future
import inverse


# Definir la session para Bybit
bybit_session = HTTP(
                    testnet=False,
                    api_key=credenciales.bybit_api_key,
                    api_secret=credenciales.bybit_api_secret,
                )

#orden = bybit_session.get_open_orders(category="linear", symbol="IOUSDT")
#orden = inverse.obtener_posicion("BYBIT","btc")
#print(json.dumps(orden,indent=2))

import os
import subprocess

# Ruta al directorio y archivo
directorio = "/Volumes/Datos/DESARROLLO PERSONAL/PROGRAMAR APLICACIONES WEB/Perfeccionar Python/Proyectos Python/Trading Bot Exchange/eva_infinity/"
archivo = "future/estrategias/infinity/infinity_2.0.py"

# Cambiar al directorio especificado y ejecutar el archivo
os.chdir(directorio)
subprocess.run(["python3", archivo])
