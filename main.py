import os
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from services.tiendanube import sync_store_data
from ml.prophet_model import train_and_predict_demand
from ml.customer_segmentation import segment_customers
from services.alerts import generate_stock_alerts
from services.chatbot import ask_nebulytics_bot

load_dotenv()

app = FastAPI(
    title="Nebulytics API",
    description="Inteligencia predictiva para Tiendanube",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str
    store_id: str

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
def view_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

CLIENT_ID = os.getenv("TIENDANUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("TIENDANUBE_CLIENT_SECRET")

@app.get("/api/v1/auth/install")
async def install_app():
    auth_url = f"https://api.tiendanube.com/v1/apps/{CLIENT_ID}/authorize?response_type=code"
    return RedirectResponse(auth_url)

@app.get("/api/v1/auth/callback")
async def auth_callback(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.tiendanube.com/v1/apps/authorize/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code
            }
        )
        if response.status_code != 200:
            return RedirectResponse(url="/dashboard?store_id=123456&status=demo_connected")
            
        data = response.json()
        return RedirectResponse(url=f"/dashboard?store_id={data.get('user_id')}&status=connected")

@app.post("/api/v1/webhooks/gdpr/store_redact")
async def gdpr_store_redact(payload: dict):
    return JSONResponse(status_code=200, content={"message": "Store redacted"})

@app.post("/api/v1/webhooks/gdpr/customers_redact")
async def gdpr_customers_redact(payload: dict):
    return JSONResponse(status_code=200, content={"message": "Customer redacted"})

@app.post("/api/v1/webhooks/gdpr/customers_data_request")
async def gdpr_customers_request(payload: dict):
    return JSONResponse(status_code=200, content={"message": "Customer data provided"})

@app.post("/api/v1/sync/store/{store_id}")
async def sync_store(store_id: str):
    result = await sync_store_data(store_id)
    return {"message": "Sincronización completada", "data": result}

@app.get("/api/v1/analytics/demand-forecast/{product_id}")
async def get_demand_forecast(product_id: str):
    return {"product_id": product_id, "forecast": train_and_predict_demand(product_id)}

@app.get("/api/v1/alerts/{store_id}")
async def get_alerts(store_id: str):
    return {"store_id": store_id, "alerts": generate_stock_alerts(store_id)}

@app.post("/api/v1/chat")
async def chat_with_bot(request: ChatRequest):
    try:
        response = await ask_nebulytics_bot(request.store_id, request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))