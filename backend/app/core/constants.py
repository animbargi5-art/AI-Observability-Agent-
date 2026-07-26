"""
===============================================================================
TattvaAI - Global Constants
===============================================================================

This module contains application-wide constant values used throughout the
TattvaAI Autonomous Incident Investigation Platform.

Guidelines:
    • Do NOT store secrets here.
    • Do NOT store environment variables here.
    • Do NOT place business logic here.
    • Do NOT hardcode strings throughout the application.

Configuration values belong in:
    core/settings.py

===============================================================================
"""

# =============================================================================
# Application
# =============================================================================

APP_AUTHOR = "TattvaAI"

APP_DESCRIPTION = (
    "AI Native Autonomous Incident Investigation Platform "
    "for Distributed Systems and AI Agents."
)

API_VERSION = "v1"

API_PREFIX = f"/api/{API_VERSION}"


# =============================================================================
# Investigation
# =============================================================================

DEFAULT_CONFIDENCE_SCORE = 0.0

MAX_CONFIDENCE_SCORE = 1.0

MIN_CONFIDENCE_SCORE = 0.0

DEFAULT_INVESTIGATION_TIMEOUT = 300  # seconds

MAX_PARALLEL_AGENTS = 10

MAX_INVESTIGATION_STEPS = 100


# =============================================================================
# Evidence Collection
# =============================================================================

MAX_EVIDENCE_PER_AGENT = 100

MAX_TOTAL_EVIDENCE = 1000

MAX_TIMELINE_EVENTS = 500

MAX_RECOMMENDATIONS = 20


# =============================================================================
# Knowledge Graph
# =============================================================================

MAX_GRAPH_NODES = 1000

MAX_GRAPH_EDGES = 5000

MAX_GRAPH_DEPTH = 10


# =============================================================================
# AI Reasoning
# =============================================================================

DEFAULT_REASONING_CONFIDENCE = 0.70

MIN_REASONING_CONFIDENCE = 0.40

HIGH_CONFIDENCE_THRESHOLD = 0.85


# =============================================================================
# Report Generation
# =============================================================================

DEFAULT_REPORT_NAME = "investigation_report"

DEFAULT_REPORT_FORMAT = "json"

REPORT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =============================================================================
# Database
# =============================================================================

DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100


# =============================================================================
# Telemetry
# =============================================================================

DEFAULT_TRACE_LIMIT = 100

DEFAULT_LOG_LIMIT = 500

DEFAULT_METRIC_LIMIT = 500

DEFAULT_ALERT_LIMIT = 100


# =============================================================================
# Time Formats
# =============================================================================

ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

DISPLAY_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"


# =============================================================================
# File Names
# =============================================================================

REPORT_DIRECTORY = "reports"

EXPORT_DIRECTORY = "exports"

LOG_DIRECTORY = "logs"


# =============================================================================
# Investigation Memory
# =============================================================================

MEMORY_KEY_EVIDENCE = "evidence"

MEMORY_KEY_TIMELINE = "timeline"

MEMORY_KEY_GRAPH = "graph"

MEMORY_KEY_FINDINGS = "findings"

MEMORY_KEY_ROOT_CAUSE = "root_cause"

MEMORY_KEY_RECOMMENDATIONS = "recommendations"

MEMORY_KEY_SUMMARY = "summary"


# =============================================================================
# LangGraph
# =============================================================================

GRAPH_START_NODE = "start"

GRAPH_END_NODE = "end"

DEFAULT_WORKFLOW_NAME = "investigation_workflow"


# =============================================================================
# SigNoz
# =============================================================================

TRACE_SEARCH_LIMIT = 100

LOG_SEARCH_LIMIT = 500

METRIC_SEARCH_LIMIT = 500

ALERT_SEARCH_LIMIT = 100


# =============================================================================
# Frontend
# =============================================================================

DEFAULT_REFRESH_INTERVAL = 5  # seconds

LIVE_UPDATE_INTERVAL = 2  # seconds


# =============================================================================
# HTTP
# =============================================================================

HTTP_OK = 200

HTTP_CREATED = 201

HTTP_ACCEPTED = 202

HTTP_BAD_REQUEST = 400

HTTP_UNAUTHORIZED = 401

HTTP_FORBIDDEN = 403

HTTP_NOT_FOUND = 404

HTTP_INTERNAL_SERVER_ERROR = 500