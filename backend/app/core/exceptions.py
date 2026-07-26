"""
===============================================================================
TattvaAI - Custom Exceptions
===============================================================================

This module defines all custom exceptions used throughout the TattvaAI
Autonomous Incident Investigation Platform.

Goals:
    • Provide meaningful exceptions
    • Improve debugging
    • Keep error handling consistent
    • Allow FastAPI to return structured error responses

===============================================================================
"""


# =============================================================================
# Base Exception
# =============================================================================

class TattvaAIError(Exception):
    """
    Base exception for the TattvaAI platform.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# =============================================================================
# Configuration Exceptions
# =============================================================================

class ConfigurationError(TattvaAIError):
    """Raised when application configuration is invalid."""
    pass


# =============================================================================
# Database Exceptions
# =============================================================================

class DatabaseError(TattvaAIError):
    """Raised when a database operation fails."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails."""
    pass


class DatabaseTransactionError(DatabaseError):
    """Raised when a database transaction fails."""
    pass


# =============================================================================
# Investigation Exceptions
# =============================================================================

class InvestigationError(TattvaAIError):
    """Base exception for investigation errors."""
    pass


class InvestigationNotFoundError(InvestigationError):
    """Raised when an investigation cannot be found."""
    pass


class InvestigationAlreadyRunningError(InvestigationError):
    """Raised when an investigation is already running."""
    pass


class InvestigationTimeoutError(InvestigationError):
    """Raised when an investigation exceeds the timeout."""
    pass


# =============================================================================
# Agent Exceptions
# =============================================================================

class AgentError(TattvaAIError):
    """Base exception for AI agent errors."""
    pass


class AgentExecutionError(AgentError):
    """Raised when an agent fails during execution."""
    pass


class AgentValidationError(AgentError):
    """Raised when agent input validation fails."""
    pass


# =============================================================================
# Evidence Exceptions
# =============================================================================

class EvidenceError(TattvaAIError):
    """Base exception for evidence-related errors."""
    pass


class EvidenceCollectionError(EvidenceError):
    """Raised when evidence collection fails."""
    pass


class InvalidEvidenceError(EvidenceError):
    """Raised when evidence is invalid."""
    pass


class CorrelationError(EvidenceError):
    """Raised when evidence correlation fails."""
    pass


# =============================================================================
# Memory Exceptions
# =============================================================================

class MemoryError(TattvaAIError):
    """Raised when Investigation Memory fails."""
    pass


# =============================================================================
# Knowledge Graph Exceptions
# =============================================================================

class KnowledgeGraphError(TattvaAIError):
    """Raised when Knowledge Graph processing fails."""
    pass


class GraphConstructionError(KnowledgeGraphError):
    """Raised while constructing the graph."""
    pass


class GraphTraversalError(KnowledgeGraphError):
    """Raised while traversing the graph."""
    pass


# =============================================================================
# Reasoning Exceptions
# =============================================================================

class ReasoningError(TattvaAIError):
    """Raised when AI reasoning fails."""
    pass


class RootCauseAnalysisError(ReasoningError):
    """Raised during root cause analysis."""
    pass


class RecommendationGenerationError(ReasoningError):
    """Raised while generating recommendations."""
    pass


# =============================================================================
# Report Exceptions
# =============================================================================

class ReportGenerationError(TattvaAIError):
    """Raised when report generation fails."""
    pass


# =============================================================================
# SigNoz Exceptions
# =============================================================================

class SigNozError(TattvaAIError):
    """Base exception for SigNoz errors."""
    pass


class SigNozConnectionError(SigNozError):
    """Raised when SigNoz cannot be reached."""
    pass


class SigNozQueryError(SigNozError):
    """Raised when a SigNoz query fails."""
    pass


# =============================================================================
# MCP Exceptions
# =============================================================================

class MCPError(TattvaAIError):
    """Base exception for MCP errors."""
    pass


class MCPConnectionError(MCPError):
    """Raised when MCP connection fails."""
    pass


class MCPAuthenticationError(MCPError):
    """Raised when MCP authentication fails."""
    pass


class MCPToolExecutionError(MCPError):
    """Raised when an MCP tool execution fails."""
    pass


# =============================================================================
# Query Builder Exceptions
# =============================================================================

class QueryBuilderError(TattvaAIError):
    """Raised when query construction fails."""
    pass


# =============================================================================
# API Exceptions
# =============================================================================

class APIError(TattvaAIError):
    """Base exception for API errors."""
    pass


class ValidationError(APIError):
    """Raised when API validation fails."""
    pass


class ResourceNotFoundError(APIError):
    """Raised when an API resource cannot be found."""
    pass