from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ml.prophet_model import get_inventory_forecast
from ml.customer_segmentation import get_customer_segments
from services.alerts import generate_stock_alerts

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    # Obtenemos los datos reales de tus modelos de IA
    forecast_data = get_inventory_forecast()
    segment_data = get_customer_segments()
    alerts = generate_stock_alerts()
    
    # Datos de productos destacados para la tabla
    top_products = [
        {"name": "Remera Urban Basic", "sales": 342, "revenue": "$684K", "trend": "+18%", "stock": 45},
        {"name": "Jean Slim Fit", "sales": 287, "revenue": "$861K", "trend": "+12%", "stock": 23},
        {"name": "Zapatillas Runner Pro", "sales": 198, "revenue": "$990K", "trend": "+25%", "stock": 8},
        {"name": "Campera Eco Light", "sales": 156, "revenue": "$780K", "trend": "-3%", "stock": 67},
    ]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "forecast": forecast_data,
        "segments": segment_data,
        "alerts": alerts,
        "products": top_products
    })
