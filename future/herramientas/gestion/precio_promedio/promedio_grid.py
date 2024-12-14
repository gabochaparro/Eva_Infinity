'''
Función que calcula el precio promedio y el precio de liquidación de un grid
'''
def promedio_grid(precio_actual, inversion, intervalo, monto_por_compra, apalancamiento):
    cantidad_grid =int(inversion*apalancamiento/monto_por_compra)
    intervalo = intervalo/100
    lista_precio = []
    lista_precio.append(precio_actual/(1+intervalo))
    sumatoria_precio = 0
    precio_promedio = 0
    precio_liquidacion = 0

    while cantidad_grid > 1:
        lista_precio.append(lista_precio[-1]/(1+intervalo))
        cantidad_grid = cantidad_grid - 1
        
    for precio in lista_precio:
        sumatoria_precio = sumatoria_precio + precio
        indice = lista_precio.index(precio)
        if indice != 0:
            if (precio_actual-lista_precio[indice])/precio_actual <= (precio_actual-precio_liquidacion)/precio_actual:
                precio_promedio = sumatoria_precio/(indice+1)
                precio_liquidacion = precio_promedio*(1-inversion/((indice+1)*monto_por_compra))
            else:
                break
        else:
            precio_promedio = sumatoria_precio
            precio_liquidacion = precio_promedio*(1-inversion/((indice+1)*monto_por_compra))
    
    print("")
    print("Inversión:", inversion, "USDT")
    print(f"Apalancamiento: {apalancamiento}x")
    print("Cantidad de grid:", indice+1)
    print(f"Rango de cobertura: ({lista_precio[0]} - {lista_precio[indice]}) ({round(100*(precio_actual-lista_precio[indice])/precio_actual,2)}%)")
    print("Precio Promedio:", precio_promedio, "(", round(100*((precio_actual-precio_promedio)/precio_actual),2),"%", ")")
    print("Precio Liquidación:", precio_liquidacion, "(", round(100*((precio_actual-precio_liquidacion)/precio_actual),2),"%", ")")
    print("")

promedio_grid(
                precio_actual=95500, 
                inversion=190, 
                intervalo=0.36+0.11, 
                monto_por_compra=200, 
                apalancamiento=9
            )