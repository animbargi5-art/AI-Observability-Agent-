from fastapi import FastAPI
import random
import time

from telemetry import setup_telemetry

app = FastAPI(title="Inventory Service")

setup_telemetry(
    app,
    "inventory-service"
)


@app.get("/")
async def home():
    return {"service": "inventory"}


@app.get("/inventory/{product_id}")
async def inventory(product_id: int):

    time.sleep(random.uniform(0.05, 0.2))

    return {
        "product": product_id,
        "stock": random.randint(1, 100)
    }