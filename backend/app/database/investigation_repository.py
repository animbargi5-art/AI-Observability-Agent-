"""
===============================================================================
TattvaAI - Investigation Repository
===============================================================================

Purpose
-------
Handles all database operations related to investigations.

Responsibilities
----------------
• Save investigation reports
• Retrieve investigations
• Delete investigations

This repository is the ONLY layer that communicates directly with the
database.

Architecture
------------
InvestigationService
        ↓
InvestigationRepository
        ↓
SQLAlchemy
        ↓
Database

===============================================================================
"""

from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError

from app.database.models import Investigation
from app.database.session import SessionLocal

from app.models.investigation_report import InvestigationReport


class InvestigationRepository:
    """
    Repository responsible for investigation persistence.
    """

    def __init__(self) -> None:

        self.db = SessionLocal()

    # -------------------------------------------------------------------------
    # Save Investigation
    # -------------------------------------------------------------------------

    def save_investigation(
        self,
        report: InvestigationReport,
    ) -> Investigation:

        try:

            investigation = Investigation(

                incident_id=report.incident_id,

                title=report.title,

                severity=report.severity,

                status=report.status,

                confidence=report.confidence,

                # Store the complete report as JSON
                report=report.model_dump(mode="json"),

            )

            self.db.add(investigation)

            self.db.commit()

            self.db.refresh(investigation)

            return investigation

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # -------------------------------------------------------------------------
    # Get All
    # -------------------------------------------------------------------------

    def get_all_investigations(
        self,
    ) -> list[Investigation]:

        return (

            self.db

            .query(Investigation)

            .all()

        )

    # -------------------------------------------------------------------------
    # Get By ID
    # -------------------------------------------------------------------------

    def get_investigation_by_id(
        self,
        investigation_id: int,
    ) -> Investigation | None:

        return (

            self.db

            .query(Investigation)

            .filter(
                Investigation.id == investigation_id
            )

            .first()

        )

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    def delete_investigation(
        self,
        investigation_id: int,
    ) -> bool:

        investigation = (

            self.db

            .query(Investigation)

            .filter(
                Investigation.id == investigation_id
            )

            .first()

        )

        if investigation is None:

            return False

        self.db.delete(investigation)

        self.db.commit()

        return True

    # -------------------------------------------------------------------------
    # Close Session
    # -------------------------------------------------------------------------

    def close(self) -> None:

        self.db.close()
