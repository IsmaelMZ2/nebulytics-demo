from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ml.prophet_model import get_inventory_forecast
from ml.customer_segmentation import get_customer_segments
from services.alerts import generate_stock_alerts

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def index(request: Request):
    # Carga inicial del Dashboard
    alerts = generate_stock_alerts("tienda_01")
    forecast = get_inventory_forecast()
    segments = get_customer_segments()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "alerts": alerts, 
        "forecast": forecast,
        "segments": segments
    })

@app.post("/chat")
async def ai_chat(data: ChatMessage):
    msg = data.message.lower()
    
    # Lógica de Orquestación de Intenciones
    if "proyecc" in msg or "ventas" in msg:
        data = get_inventory_forecast()
        return {
            "reply": "He analizado las tendencias. Se espera un crecimiento del 15% en los ingresos para el próximo mes. He actualizado la gráfica central para que veas el detalle.",
            "action": "UPDATE_CHART",
            "payload": data
        }
    elif "stock" in msg or "alerta" in msg:
        alerts = generate_stock_alerts("tienda_01")
        return {
            "reply": f"Tienes {len(alerts)} alertas críticas. El producto 'Camiseta Básica' requiere reabastecimiento urgente.",
            "action": "HIGHLIGHT_ALERTS",
            "payload": alerts
        }
    
    return {
        "reply": "Soy Nebulytics IA. Puedo analizar tus ventas, predecir stock o segmentar a tus clientes. ¿Qué prefieres ver?",
        "action": "NONE"
    }
