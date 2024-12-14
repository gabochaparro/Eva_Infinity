import os
import subprocess

# Ruta al directorio y archivo
directorio = "/Volumes/Datos/DESARROLLO PERSONAL/PROGRAMAR APLICACIONES WEB/Perfeccionar Python/Proyectos Python/Trading Bot Exchange/exchange/"
archivo = "future/estrategias/infinity/infinity_2.0.py"

# Cambiar al directorio especificado y ejecutar el archivo
os.chdir(directorio)
subprocess.run(["python3", archivo])
