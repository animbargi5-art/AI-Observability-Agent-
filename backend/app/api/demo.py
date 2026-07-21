import time 
import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/demo",
    tags=["Demo APIs"]
)

@router.get("/healthy")
def healthy():

    logger.info("Healthy endpoint called.")

    return {
        "status": "healthy",
        "message": "Everything is operating normally."
    }

@router.get("/slow")
def slow():

    logger.info("Slow endpoint started.")

    time.sleep(3)

    logger.warning("Slow endpoint exceeded expected response time.")

    return {
        "status": "success",
        "message": "Slow endpoint completed.",
        "delay_seconds": 3
    }

@router.get("/error")
def error():

    logger.error("Demo endpoint generated Internal Server Error.")

    raise HTTPException(
        status_code=500,
        detail="Internal Server Error (Demo)"
    )