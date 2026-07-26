"""
===============================================================================
TattvaAI - Log Domain Model
===============================================================================

Represents a normalized application log used throughout the
TattvaAI investigation pipeline.

This model is transport-independent and represents the canonical
log object inside TattvaAI.

Every log retrieved from SigNoz, OpenTelemetry, Loki, ELK, or any
other logging system must first be converted into this model before
being consumed by the investigation pipeline.

Flow
----
SigNoz / OpenTelemetry / Loki
        ↓
MCP Gateway
        ↓
Telemetry Service
        ↓
Logs Tool
        ↓
Log
        ↓
Logs Agent
        ↓
Evidence

===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Log(BaseModel):
    """
    Canonical application log.
    """

    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------

    log_id: Optional[str] = None

    trace_id: Optional[str] = None

    span_id: Optional[str] = None

    # -------------------------------------------------------------------------
    # Service Information
    # -------------------------------------------------------------------------

    service_name: str

    host: Optional[str] = None

    environment: Optional[str] = None

    namespace: Optional[str] = None

    service_version: Optional[str] = None

    # -------------------------------------------------------------------------
    # Log Information
    # -------------------------------------------------------------------------

    severity: str

    message: str

    logger_name: Optional[str] = None

    # -------------------------------------------------------------------------
    # Exception Information
    # -------------------------------------------------------------------------

    exception_type: Optional[str] = None

    exception_message: Optional[str] = None

    stacktrace: Optional[str] = None

    # -------------------------------------------------------------------------
    # Source Information
    # -------------------------------------------------------------------------

    file_name: Optional[str] = None

    function_name: Optional[str] = None

    line_number: Optional[int] = None

    thread_name: Optional[str] = None

    process_id: Optional[int] = None

    # -------------------------------------------------------------------------
    # Timing
    # -------------------------------------------------------------------------

    timestamp: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Additional Attributes
    # -------------------------------------------------------------------------

    attributes: dict[str, str] = Field(
        default_factory=dict
    )

    # -------------------------------------------------------------------------
    # Helper Properties
    # -------------------------------------------------------------------------

    @property
    def is_error(self) -> bool:
        """
        Returns True when the log severity is ERROR.
        """
        return self.severity.upper() == "ERROR"

    @property
    def is_warning(self) -> bool:
        """
        Returns True when the log severity is WARNING.
        """
        return self.severity.upper() in (
            "WARN",
            "WARNING",
        )

    @property
    def is_info(self) -> bool:
        """
        Returns True when the log severity is INFO.
        """
        return self.severity.upper() == "INFO"

    @property
    def is_debug(self) -> bool:
        """
        Returns True when the log severity is DEBUG.
        """
        return self.severity.upper() == "DEBUG"

    @property
    def is_critical(self) -> bool:
        """
        Returns True when the log severity is CRITICAL.
        """
        return self.severity.upper() == "CRITICAL"

    @property
    def has_exception(self) -> bool:
        """
        Returns True when exception information is present.
        """
        return self.exception_type is not None

    @property
    def has_trace(self) -> bool:
        """
        Returns True when this log is linked to a distributed trace.
        """
        return self.trace_id is not None

    @property
    def severity_score(self) -> int:
        """
        Converts severity into a numeric score.
        """

        scores = {
            "DEBUG": 10,
            "INFO": 20,
            "WARN": 40,
            "WARNING": 40,
            "ERROR": 70,
            "CRITICAL": 100,
        }

        return scores.get(self.severity.upper(), 0)

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def summary(self) -> str:
        """
        Returns a concise human-readable summary.
        """

        return (
            f"[{self.severity}] "
            f"{self.service_name} : "
            f"{self.message}"
        )