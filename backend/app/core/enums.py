"""
===============================================================================
TattvaAI - Core Enums
===============================================================================

This module contains all application-wide enumerations used throughout the
TattvaAI Autonomous Incident Investigation Platform.

Purpose:
    - Eliminate hardcoded string values
    - Improve code readability
    - Ensure type safety
    - Provide consistency across Backend, API, Database, and Frontend

Author:
    TattvaAI

===============================================================================
"""

from enum import Enum


# =============================================================================
# Investigation Status
# =============================================================================

class InvestigationStatus(str, Enum):
    """
    Overall lifecycle status of an investigation.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# =============================================================================
# Investigation Stage
# =============================================================================

class InvestigationStage(str, Enum):
    """
    Current processing stage of the investigation.
    """

    INITIALIZED = "INITIALIZED"

    COLLECTING_EVIDENCE = "COLLECTING_EVIDENCE"

    CORRELATING_EVIDENCE = "CORRELATING_EVIDENCE"

    BUILDING_GRAPH = "BUILDING_GRAPH"

    ANALYZING = "ANALYZING"

    ROOT_CAUSE_ANALYSIS = "ROOT_CAUSE_ANALYSIS"

    GENERATING_RECOMMENDATIONS = "GENERATING_RECOMMENDATIONS"

    GENERATING_REPORT = "GENERATING_REPORT"

    COMPLETED = "COMPLETED"


# =============================================================================
# Severity
# =============================================================================

class Severity(str, Enum):
    """
    Severity level of an incident.
    """

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


# =============================================================================
# Agent Types
# =============================================================================

class AgentType(str, Enum):
    """
    Types of AI agents available inside TattvaAI.
    """

    COORDINATOR = "COORDINATOR"

    TRACE = "TRACE"

    LOGS = "LOGS"

    METRICS = "METRICS"

    ALERT = "ALERT"

    DEPENDENCY = "DEPENDENCY"

    HISTORICAL = "HISTORICAL"

    ROOT_CAUSE = "ROOT_CAUSE"

    RECOMMENDATION = "RECOMMENDATION"

    REPORT = "REPORT"


# =============================================================================
# Agent State
# =============================================================================

class AgentState(str, Enum):
    """
    Runtime execution state of an agent.
    """

    WAITING = "WAITING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


# =============================================================================
# Evidence Types
# =============================================================================

class EvidenceType(str, Enum):
    """
    Types of evidence collected during an investigation.
    """

    TRACE = "TRACE"

    LOG = "LOG"

    METRIC = "METRIC"

    ALERT = "ALERT"

    DEPENDENCY = "DEPENDENCY"

    HISTORICAL = "HISTORICAL"


# =============================================================================
# Recommendation Priority
# =============================================================================

class RecommendationPriority(str, Enum):
    """
    Priority of generated recommendations.
    """

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


# =============================================================================
# Recommendation Type
# =============================================================================

class RecommendationType(str, Enum):
    """
    Categories of recommendations.
    """

    IMMEDIATE = "IMMEDIATE"

    SHORT_TERM = "SHORT_TERM"

    LONG_TERM = "LONG_TERM"

    PREVENTIVE = "PREVENTIVE"


# =============================================================================
# Report Format
# =============================================================================

class ReportFormat(str, Enum):
    """
    Supported report export formats.
    """

    JSON = "JSON"

    PDF = "PDF"

    HTML = "HTML"

    MARKDOWN = "MARKDOWN"


# =============================================================================
# Investigation Result
# =============================================================================

class InvestigationResult(str, Enum):
    """
    Final outcome of an investigation.
    """

    SUCCESS = "SUCCESS"

    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"

    FAILED = "FAILED"


# =============================================================================
# Graph Node Type
# =============================================================================

class GraphNodeType(str, Enum):
    """
    Node types inside the Evidence Knowledge Graph.
    """

    SERVICE = "SERVICE"

    TRACE = "TRACE"

    SPAN = "SPAN"

    LOG = "LOG"

    METRIC = "METRIC"

    ALERT = "ALERT"

    DATABASE = "DATABASE"

    CACHE = "CACHE"

    API = "API"

    DEPLOYMENT = "DEPLOYMENT"

    ROOT_CAUSE = "ROOT_CAUSE"


# =============================================================================
# Graph Edge Type
# =============================================================================

class GraphEdgeType(str, Enum):
    """
    Relationship types between graph nodes.
    """

    CALLS = "CALLS"

    DEPENDS_ON = "DEPENDS_ON"

    GENERATED = "GENERATED"

    CAUSED_BY = "CAUSED_BY"

    CONNECTED_TO = "CONNECTED_TO"

    RELATED_TO = "RELATED_TO"


# =============================================================================
# Timeline Event
# =============================================================================

class TimelineEventType(str, Enum):
    """
    Types of events shown on the investigation timeline.
    """

    INCIDENT_CREATED = "INCIDENT_CREATED"

    AGENT_STARTED = "AGENT_STARTED"

    AGENT_COMPLETED = "AGENT_COMPLETED"

    EVIDENCE_COLLECTED = "EVIDENCE_COLLECTED"

    CORRELATION_COMPLETED = "CORRELATION_COMPLETED"

    ROOT_CAUSE_IDENTIFIED = "ROOT_CAUSE_IDENTIFIED"

    RECOMMENDATIONS_GENERATED = "RECOMMENDATIONS_GENERATED"

    REPORT_GENERATED = "REPORT_GENERATED"

    INVESTIGATION_COMPLETED = "INVESTIGATION_COMPLETED"