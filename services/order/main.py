from fastapi import FastAPI
import httpx

from telemetry import setup_telemetry

app = FastAPI(
    title="Order Service"
)

setup_telemetry(
    app,
    "order-service"
)


@app.get("/")
async def home():

    return {
        "service": "order"
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "order"}


@app.get("/orders")
async def get_orders():

    orders = [
        {
            "id": 1,
            "product_id": 101,
            "product": "Laptop"
        },
        {
            "id": 2,
            "product_id": 102,
            "product": "Mouse"
        }
    ]

    async with httpx.AsyncClient() as client:

        for order in orders:

            inventory = await client.get(
                f"http://inventory:8000/inventory/{order['id']}"
            )

            payment = await client.get(
                f"http://payment:8000/pay/{order['id']}"
            )

            order["inventory"] = inventory.json()

            order["payment"] = payment.json()

    return {
        "orders": orders
    }
