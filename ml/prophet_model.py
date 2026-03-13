import math
from datetime import datetime, timedelta

def get_inventory_forecast(): # <-- Cambiamos el nombre aquí
    data = []
    base_date = datetime.now() - timedelta(days=30)
    for i in range(45):
        current_date = base_date + timedelta(days=i)
        tendencia = 15 + (i * 0.5)
        ruido = math.sin(i * 0.5) * 5
        valor = max(0, int(tendencia + ruido))
        
        if i >= 30:
            data.append({
                'ds': current_date.strftime('%Y-%m-%d'), 
                'yhat': valor, 
                'yhat_lower': max(0, valor - 3), 
                'yhat_upper': valor + 4
            })
        else:
            data.append({
                'ds': current_date.strftime('%Y-%m-%d'), 
                'actual': valor, 
                'yhat': valor
            })
    return data
