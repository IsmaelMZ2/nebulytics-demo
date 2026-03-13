def get_customer_segments():
    """Simulación de segmentación de clientes para el Dashboard"""
    return {
        "status": "success",
        "segments": {
            "Clientes VIP": 15,
            "Clientes Frecuentes": 45,
            "Nuevos Clientes": 30,
            "Clientes en Riesgo": 10
        },
        "total": 100,
        "recomendacion": "Ofrecer un cupón de recompra al segmento 'En Riesgo' para evitar su pérdida."
    }
