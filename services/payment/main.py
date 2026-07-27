import random
import time

from fastapi import FastAPI, HTTPException

from telemetry import setup_telemetry

app = FastAPI(
    title="Payment Service"
)

setup_telemetry(
    app,
    "payment-service"
)


@app.get("/")
async def home():
    return {
        "service": "payment"
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "payment"}


@app.get("/pay/{order_id}")
async def pay(order_id: int):

    delay = random.uniform(0.2, 3.0)

    time.sleep(delay)

    # 25% chance of failure
    if random.randint(1, 4) == 1:

        raise HTTPException(
            status_code=500,
            detail="Payment Gateway Timeout"
        )

    return {
        "status": "paid",
        "order_id": order_id,
        "processing_time": round(delay, 2)
    }
