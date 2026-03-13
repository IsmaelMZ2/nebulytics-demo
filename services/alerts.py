from typing import List

def get_db_metrics(store_id: str):
    return [
        {"product_id": "P01", "name": "Camiseta Básica", "stock": 5, "daily_avg_sales": 2.5},
        {"product_id": "P02", "name": "Zapatillas Run", "stock": 400, "daily_avg_sales": 1.0},
    ]

def generate_stock_alerts(store_id: str) -> List[dict]:
    metrics = get_db_metrics(store_id)
    alerts = []
    
    for item in metrics:
        days_left = item["stock"] / item["daily_avg_sales"] if item["daily_avg_sales"] > 0 else 999
        if days_left <= 3:
            alerts.append({"type": "CRITICAL_STOCK", "message": f"'{item['name']}' se agotará en {int(days_left)} días. ¡Reabastece pronto!", "color": "red"})
        elif item["stock"] > 300 and item["daily_avg_sales"] < 2:
            alerts.append({"type": "OVERSTOCK", "message": f"Exceso de stock en '{item['name']}'. Aplica descuento del 15%.", "color": "yellow"})
            
    alerts.append({"type": "CART_ABANDONED", "message": "15 carritos abandonados hoy ($1,200). Envia campaña de recuperación.", "color": "blue"})
    return alerts
