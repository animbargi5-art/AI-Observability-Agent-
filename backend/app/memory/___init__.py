"""
===============================================================================
TattvaAI - Memory Package
===============================================================================

The Memory package provides the shared investigation memory used throughout
the TattvaAI Autonomous Incident Investigation Platform.

It enables AI agents to collaborate by sharing a common InvestigationState.

Modules
-------
investigation_memory
    Shared memory implementation.

manager
    Investigation memory lifecycle manager.

===============================================================================
"""

from .investigation_memory import InvestigationMemory
from .manager import MemoryManager

__all__ = [
    "InvestigationMemory",
    "MemoryManager",
]