import os
from openai import AsyncOpenAI
from services.alerts import generate_stock_alerts

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_nebulytics_bot(store_id: str, user_message: str):
    alerts = generate_stock_alerts(store_id)
    alerts_context = "\n".join([f"- {a['type']}: {a['message']}" for a in alerts])
    
    system_prompt = f"""
    Eres el asistente de negocios inteligente de Nebulytics. 
    Traduce datos de inventario en recomendaciones accionables.
    Contexto de la tienda (Alertas de stock actuales): {alerts_context}
    Responde en español, sé directo, conciso y orientando a la acción.
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Actualmente estoy sincronizando los inventarios. Por favor, intenta de nuevo."
