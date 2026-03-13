import os

def get_auth_url():
    """Genera la URL para que el usuario autorice la app en Tiendanube"""
    client_id = os.getenv("TIENDANUBE_CLIENT_ID", "12345")
    # URL de redirección base para la demo
    return f"https://www.tiendanube.com/apps/{client_id}/authorize"

async def handle_callback(code: str):
    """Simula el intercambio del código por un token de acceso"""
    # Para el Hackathon, devolvemos un token simulado si no hay API oficial lista
    return {
        "access_token": "shpat_demo_token_123456789",
        "scope": "read_products,write_products",
        "user_id": "12345"
    }