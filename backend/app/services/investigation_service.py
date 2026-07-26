"""
===============================================================================
TattvaAI - Investigation Service
===============================================================================

Purpose
-------
Business service responsible for investigation persistence.

Responsibilities
----------------
• Save investigation reports
• Retrieve investigations
• Delete investigations

This service contains NO database logic.

Architecture
------------
Coordinator
      ↓
InvestigationService
      ↓
InvestigationRepository
      ↓
Database

===============================================================================
"""

from __future__ import annotations

from app.database.investigation_repository import (
    InvestigationRepository,
)

from app.models.investigation_report import (
    InvestigationReport,
)


class InvestigationService:
    """
    Business service for investigation persistence.
    """

    def __init__(self) -> None:

        self.repository = InvestigationRepository()

    # -------------------------------------------------------------------------
    # Save
    # -------------------------------------------------------------------------

    def save(
        self,
        report: InvestigationReport,
    ):
        """
        Save an investigation report.
        """

        return self.repository.save_investigation(
            report
        )

    # -------------------------------------------------------------------------
    # Retrieve
    # -------------------------------------------------------------------------

    def get_all_investigations(
        self,
    ):
        """
        Return every stored investigation.
        """

        return self.repository.get_all_investigations()

    def get_investigation_by_id(
        self,
        investigation_id: int,
    ):
        """
        Retrieve one investigation.
        """

        return self.repository.get_investigation_by_id(
            investigation_id
        )

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    def delete_investigation(
        self,
        investigation_id: int,
    ):
        """
        Delete one investigation.
        """

        return self.repository.delete_investigation(
            investigation_id
        )