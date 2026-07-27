"""
Dashboard API endpoints for TattvaAI frontend.
Provides dashboard statistics, recent investigations, and system status.
"""

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Query

from app.core.settings import settings
from app.services.investigation_store import investigation_store

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/recent")
async def get_recent_investigations(limit: int = Query(default=10, ge=1, le=50)):
    """Get recent investigations for dashboard."""
    
    # In demo mode, return mock recent investigations
    if settings.DEMO_MODE:
        investigations = []
        
        for i in range(min(limit, 5)):
            investigation = {
                "id": f"inv_{i+1}",
                "service_name": "gateway" if i % 2 == 0 else "payment",
                "status": "COMPLETED" if i < 3 else "IN_PROGRESS",
                "severity": "HIGH" if i == 0 else "MEDIUM",
                "created_at": (datetime.now() - timedelta(hours=i * 2)).isoformat(),
                "updated_at": (datetime.now() - timedelta(hours=i * 2 - 1)).isoformat(),
                "root_cause": "Database connection timeout" if i == 0 else None,
                "confidence": 0.95 if i == 0 else 0.8,
                "affected_services": ["gateway", "database"] if i == 0 else ["payment"]
            }
            investigations.append(investigation)
        
        return {
            "investigations": investigations,
            "total": len(investigations)
        }
    
    investigations = investigation_store.list(limit)
    return {"investigations": investigations, "total": len(investigations)}


@router.get("/statistics")
async def get_dashboard_statistics():
    """Get dashboard statistics."""
    
    # In demo mode, return mock statistics
    if settings.DEMO_MODE:
        return {
            "total_investigations": 47,
            "active_investigations": 3,
            "resolved_today": 8,
            "average_resolution_time": "2.3h",
            "success_rate": 94.5,
            "services_monitored": 12,
            "alerts_last_24h": 15,
            "critical_incidents": 2
        }
    
    investigations = investigation_store.list()
    completed = [item for item in investigations if item.get("status") == "COMPLETED"]
    return {
        "total_investigations": len(investigations),
        "active_investigations": sum(item.get("status") == "IN_PROGRESS" for item in investigations),
        "resolved_today": len(completed),
        "average_resolution_time": "0h",
        "success_rate": round((len(completed) / len(investigations) * 100), 1) if investigations else 0,
        "services_monitored": len({item.get("service_name") for item in investigations}),
        "alerts_last_24h": sum(len(item.get("alerts", [])) for item in investigations),
        "critical_incidents": sum(item.get("severity") == "CRITICAL" for item in investigations)
    }


@router.get("/signoz-status")
async def get_signoz_status():
    """Get SigNoz connection status."""
    
    # In demo mode, return mock status
    if settings.DEMO_MODE:
        return {
            "status": "connected",
            "version": "0.55.0",
            "last_check": datetime.now().isoformat(),
            "services_count": 12,
            "traces_last_hour": 45678,
            "logs_last_hour": 123456,
            "metrics_last_hour": 987654
        }
    
    return {
        "status": "connected",
        "version": None,
        "last_check": datetime.now().isoformat(),
        "services_count": 0,
        "traces_last_hour": 0,
        "logs_last_hour": 0,
        "metrics_last_hour": 0
    }


@router.get("/health-overview")
async def get_health_overview():
    """Get overall system health overview."""
    
    # In demo mode, return mock health data
    if settings.DEMO_MODE:
        services = [
            {"name": "gateway", "status": "healthy", "response_time": 45, "error_rate": 0.1},
            {"name": "inventory", "status": "healthy", "response_time": 32, "error_rate": 0.0},
            {"name": "order", "status": "degraded", "response_time": 156, "error_rate": 2.3},
            {"name": "payment", "status": "healthy", "response_time": 67, "error_rate": 0.2},
        ]
        
        return {
            "services": services,
            "overall_status": "degraded",
            "healthy_services": 3,
            "total_services": 4,
            "average_response_time": 75,
            "total_error_rate": 0.65
        }
    
    # TODO: When not in demo mode, get real health data
    return {
        "services": [],
        "overall_status": "unknown",
        "healthy_services": 0,
        "total_services": 0,
        "average_response_time": 0,
        "total_error_rate": 0
    }
