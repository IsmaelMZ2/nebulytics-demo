import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

# Importamos las piezas que movimos a las carpetas
from services.auth import get_auth_url, handle_callback
from services.tiendanube import sync_store_data
from services.chatbot import ask_nebulytics_bot
from ml.prophet_model import get_inventory_forecast
from ml.customer_segmentation import get_customer_segments

app = FastAPI(title="Nebulytics API")

# 1. Configuración de Archivos Estáticos y Plantillas
# Esto permite que Render encuentre tu CSS, JS e HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- RUTAS DE NAVEGACIÓN (FRONTEND) ---

@app.get("/")
async def read_root(request: Request):
    """Página de aterrizaje (Landing Page)"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
async def read_dashboard(request: Request):
    """Panel de control principal con gráficas de IA"""
    # Aquí simulamos datos para la demo del hackathon
    forecast = get_inventory_forecast()
    segments = get_customer_segments()
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "forecast": forecast,
        "segments": segments
    })

# --- RUTAS DE AUTENTICACIÓN (TIENDANUBE) ---

@app.get("/api/v1/auth/install")
async def install(request: Request):
    """Punto de inicio para instalar la app en Tiendanube"""
    auth_url = get_auth_url()
    return JSONResponse({"url": auth_url})

@app.get("/api/v1/auth/callback")
async def callback(code: str):
    """Recibe el código de Tiendanube y activa la sincronización"""
    token_data = await handle_callback(code)
    # Iniciamos la carga de datos en segundo plano
    await sync_store_data(token_data['access_token'])
    return {"status": "success", "message": "Tienda conectada con éxito"}

# --- RUTAS DE INTELIGENCIA ARTIFICIAL (CHATBOT) ---

@app.post("/api/v1/chatbot/ask")
async def chat(request: Request):
    """Endpoint que consume el widget.js que pusimos en static"""
    data = await request.json()
    user_message = data.get("message")
    store_id = data.get("store_id", "demo_123")
    
    response = await ask_nebulytics_bot(store_id, user_message)
    return {"response": response}

# --- INICIO DEL SERVIDOR ---
if __name__ == "__main__":
    import uvicorn
    # Render usa el puerto que le asigne el sistema ($PORT)
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)