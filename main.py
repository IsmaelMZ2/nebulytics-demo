from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ml.prophet_model import get_inventory_forecast
from ml.customer_segmentation import get_customer_segments
from services.alerts import generate_stock_alerts # Importamos tu función

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def dashboard(request: Request):
    # 1. Llamamos a tu lógica de alertas con un ID de prueba
    alerts_data = generate_stock_alerts(store_id="tienda_demo_01")
    
    # 2. Obtenemos datos de IA
    forecast = get_inventory_forecast()
    segments = get_customer_segments()

    # 3. Datos para la tabla de productos (estáticos para la demo)
    products = [
        {"name": "Remera Urban Basic", "sales": 342, "rev": "$684K", "trend": "+18%", "stock": 45},
        {"name": "Jean Slim Fit", "sales": 287, "rev": "$861K", "trend": "+12%", "stock": 23},
        {"name": "Zapatillas Runner Pro", "sales": 198, "rev": "$990K", "trend": "+25%", "stock": 8},
        {"name": "Campera Eco Light", "sales": 156, "rev": "$780K", "trend": "-3%", "stock": 67},
    ]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "alerts": alerts_data,
        "forecast": forecast,
        "segments": segments,
        "products": products
    })
