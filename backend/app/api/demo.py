import time
import random
import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/demo",
    tags=["Demo APIs"]
)


@router.get("/healthy")
def healthy():
    """
    Normal healthy endpoint.
    """

    logger.info("Healthy endpoint called.")

    return {
        "status": "healthy",
        "message": "Everything is operating normally."
    }


@router.get("/slow")
def slow():
    """
    Simulates a slow API.
    """

    logger.info("Slow endpoint started.")

    time.sleep(3)

    logger.warning("Slow endpoint exceeded expected response time.")

    return {
        "status": "success",
        "message": "Slow endpoint completed.",
        "delay_seconds": 3
    }


@router.get("/very-slow")
def very_slow():
    """
    Simulates a critically slow API.
    """

    logger.info("Very slow endpoint started.")

    time.sleep(6)

    logger.error("Very slow endpoint exceeded critical latency threshold.")

    return {
        "status": "success",
        "message": "Very slow endpoint completed.",
        "delay_seconds": 6
    }


@router.get("/error")
def error():
    """
    Simulates a server error.
    """

    logger.error("Demo endpoint generated Internal Server Error.")

    raise HTTPException(
        status_code=500,
        detail="Internal Server Error (Demo)"
    )


@router.get("/client-error")
def client_error():
    """
    Simulates a client-side request error.
    """

    logger.warning("Client submitted an invalid request.")

    raise HTTPException(
        status_code=400,
        detail="Bad Request (Demo)"
    )


@router.get("/database")
def database():
    """
    Simulates a slow database query.
    """

    logger.info("Connecting to database...")

    time.sleep(2)

    logger.warning("Database query took longer than expected.")

    return {
        "status": "success",
        "database": "connected",
        "query_time_seconds": 2
    }


@router.get("/payment")
def payment():
    """
    Simulates payment processing.
    """

    logger.info("Payment processing started.")

    time.sleep(1.5)

    logger.info("Payment processed successfully.")

    return {
        "status": "paid"
    }


@router.get("/inventory")
def inventory():
    """
    Simulates inventory lookup.
    """

    logger.info("Inventory lookup started.")

    time.sleep(1)

    return {
        "items": 143
    }


@router.get("/random")
def random_endpoint():
    """
    Generates random behavior.
    Useful for producing realistic telemetry.
    """

    value = random.randint(1, 5)

    if value == 1:

        logger.info("Random endpoint returned healthy response.")

        return {
            "status": "healthy"
        }

    elif value == 2:

        logger.warning("Random endpoint became slow.")

        time.sleep(4)

        return {
            "status": "slow"
        }

    elif value == 3:

        logger.error("Random endpoint produced server error.")

        raise HTTPException(
            status_code=500,
            detail="Random Failure"
        )

    elif value == 4:

        logger.warning("Random endpoint produced client error.")

        raise HTTPException(
            status_code=404,
            detail="Resource Not Found"
        )

    logger.info("Random endpoint completed normally.")

    return {
        "status": "normal"
    }