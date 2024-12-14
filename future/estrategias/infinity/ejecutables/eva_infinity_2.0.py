import json
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import os

# Función para cargar el archivo JSON
def cargar_json():
    global data, ruta_archivo, ultima_modificacion, nombre_archivo, ventana, frame_editor
    try:
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if archivo:
            nombre_archivo = archivo.split("/")[-1]
            ventana.title(f"Eva Infinity 2.0 - {nombre_archivo}")
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            ruta_archivo = archivo
            ultima_modificacion = os.path.getmtime(ruta_archivo)
            actualizar_interfaz()
            messagebox.showinfo("Carga exitosa", "Archivo cargado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

# Función que actualiza la interfaz
def actualizar_interfaz():
    for widget in frame_editor.winfo_children():
        widget.destroy()  # Limpiar el frame antes de cargar nuevos valores
    entries.clear()
    botones_booleanos.clear()

    if data['inverso']:
        base_coin = data['activo']
    else:
        base_coin = "USDT"

    for i, (clave, valor) in enumerate(data.items()):

        # Mostrar clave como texto no editable
        if clave == 'balance_inicial':
            tk.Label(frame_editor, text=f"Balance Inicial ({base_coin}):", anchor="w", width=27).grid(row=0, column=0, padx=1.8, pady=1.8)
            if data['inverso']:
                label_valor = tk.Label(frame_editor, text=round(float(data['balance_inicial']), 8), anchor="w", width=9)
            else:
                label_valor = tk.Label(frame_editor, text=round(float(data['balance_inicial']), 2), anchor="w", width=9)
            label_valor.grid(row=0, column=1, padx=1.8, pady=1.8)

        if clave == 'balance_actual':
            tk.Label(frame_editor, text=f"Balance Actual ({base_coin}):", anchor="w", width=27).grid(row=1, column=0, padx=1.8, pady=1.8)
            if data['inverso']:
                label_valor = tk.Label(frame_editor, text=round(float(data['balance_actual']), 8), anchor="w", width=9)
            else:
                label_valor = tk.Label(frame_editor, text=round(float(data['balance_actual']), 2), anchor="w", width=9)
            label_valor.grid(row=1, column=1, padx=1.8, pady=1.8)

        if 'balance_inicial' != clave != 'balance_actual':
            tk.Label(frame_editor, text=f"{clave}:", anchor="w", width=27).grid(row=i + 2, column=0, padx=1.8, pady=1.8)

            if isinstance(valor, bool):  # Crear un botón toggle para valores booleanos
                if clave == 'pausa':
                    if valor:
                        btn_toggle = tk.Button(frame_editor, text="Sí" if valor else "No", width=6, fg="red", bg="red", 
                                               command=lambda c=clave: toggle_boolean(c))
                    else:
                        btn_toggle = tk.Button(frame_editor, text="Sí" if valor else "No", width=6, fg="green", bg="green",
                                               command=lambda c=clave: toggle_boolean(c))
                else:
                    btn_toggle = tk.Button(frame_editor, text="Sí" if valor else "No", width=6, 
                                           command=lambda c=clave: toggle_boolean(c))
                btn_toggle.grid(row=i + 2, column=1, padx=1.8, pady=1.8)
                botones_booleanos[clave] = btn_toggle

            elif clave == 'direccion':  # Usar OptionMenu para LONG, RANGO, SHORT
                opciones = ["LONG", "RANGO", "SHORT"]
                valor_actual = "RANGO" if valor == "" else str(valor).upper()
                seleccion = tk.StringVar(value=valor_actual)

                def actualizar_direccion(*args, clave=clave):
                    data[clave] = "" if seleccion.get() == "RANGO" else seleccion.get()
                    # Cambiar color según la dirección seleccionada
                    color = "green" if seleccion.get() == "LONG" else "yellow" if seleccion.get() == "RANGO" else "red"
                    menu.config(bg=color)

                seleccion.trace("w", actualizar_direccion)
                menu = tk.OptionMenu(frame_editor, seleccion, *opciones)
                menu.config(width=5, fg="black", bg="green" if valor_actual == "LONG" else "yellow" if valor_actual == "RANGO" else "red")
                menu.grid(row=i + 2, column=1, padx=0.9, pady=0.9)

            elif clave == 'exchange':  # Usar OptionMenu para BYBIT y BINANCE
                if nombre_archivo == "parametros_infinity_2.0.json":
                    opciones_exchange = ["BYBIT", "BINANCE"]
                    seleccion_exchange = tk.StringVar(value=str(valor).upper())

                    def actualizar_exchange(*args, clave=clave):
                        data[clave] = seleccion_exchange.get()

                    seleccion_exchange.trace("w", actualizar_exchange)
                    menu_exchange = tk.OptionMenu(frame_editor, seleccion_exchange, *opciones_exchange)
                    menu_exchange.config(width=5)
                    menu_exchange.grid(row=i + 2, column=1, padx=1.8, pady=1.8)
                else:
                    label_valor = tk.Label(frame_editor, text=str(valor).upper(), anchor="w", width=9)
                    label_valor.grid(row=i + 2, column=1, padx=1.8, pady=1.8)

            elif clave == 'activo':  # Campo editable solo si es el archivo permitido
                if nombre_archivo == "parametros_infinity_2.0.json":
                    entry = tk.Entry(frame_editor, width=9)
                    entry.insert(0, str(valor).upper())
                    entry.grid(row=i + 2, column=1, padx=1.8, pady=1.8)
                    entries[clave] = entry
                else:
                    label_valor = tk.Label(frame_editor, text=str(valor).upper(), anchor="w", width=9)
                    label_valor.grid(row=i + 2, column=1, padx=1.8, pady=1.8)

            else:  # Otros tipos (int, float, etc.) como campos editables
                entry = tk.Entry(frame_editor, width=9)
                entry.insert(0, str(valor).upper())
                entry.grid(row=i + 2, column=1, padx=1.8, pady=1.8)
                entries[clave] = entry

# Función para alternar valores booleanos
def toggle_boolean(clave):
    if clave != "inverso" or nombre_archivo == "parametros_infinity_2.0.json":
        valor_actual = data[clave]
        data[clave] = not valor_actual  # Alternar entre True y False
        btn_toggle = botones_booleanos[clave]
        btn_toggle.config(text="Sí" if data[clave] else "No")

# Función para guardar cambios en el archivo JSON
def guardar_json():
    try:
        for clave, entry in entries.items():
            valor = entry.get()
            try:
                data[clave] = eval(valor)  # Convertir al tipo adecuado
            except:
                data[clave] = valor  # Mantener como string si falla la conversión

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Guardado exitoso", "Archivo guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

# Función para monitorear cambios en el archivo JSON
def monitorear_cambios():
    global ultima_modificacion, ruta_archivo, data
    while True:
        if ruta_archivo:
            try:
                mod_time = os.path.getmtime(ruta_archivo)
                if mod_time != ultima_modificacion:  # Detectar cambios en la marca de tiempo
                    ultima_modificacion = mod_time
                    with open(ruta_archivo, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    ventana.after(0, actualizar_interfaz)  # Actualizar la interfaz en el hilo principal
            except Exception as e:
                print(f"Error monitoreando el archivo: {e}")
        time.sleep(1)  # Verificar cada segundo

# Configurar la ventana principal
ventana = tk.Tk()
ventana.title(f"Eva Infinity 2.0")
ventana.geometry("369x720")
ventana.resizable(True, True)

# Botones de carga y guardado
boton_cargar = tk.Button(ventana, text="Cargar", command=cargar_json)
boton_cargar.pack(pady=5)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_json)
boton_guardar.pack(pady=5)

# Frame para los editores de claves y valores
frame_editor = tk.Frame(ventana)
frame_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Variables globales
data = {}
ruta_archivo = None
ultima_modificacion = None
entries = {}  # Para campos editables no booleanos
botones_booleanos = {}  # Para botones toggle

# Iniciar el monitoreo en un hilo aparte
hilo_monitoreo = threading.Thread(target=monitorear_cambios, daemon=True)
hilo_monitoreo.start()

# Iniciar la aplicación
ventana.mainloop()
