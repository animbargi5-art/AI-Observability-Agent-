from fastapi import FastAPI
import httpx

from telemetry import setup_telemetry

app = FastAPI(
    title="Gateway Service"
)

setup_telemetry(
    app,
    "gateway-service"
)

@app.get("/")
async def home():

    return {
        "service": "gateway"
    }

@app.get("/orders")
async def get_orders():

    print("Gateway received request")

    async with httpx.AsyncClient() as client:

        response = await client.get(
            "http://127.0.0.1:8101/orders"
        )

        return response.json()