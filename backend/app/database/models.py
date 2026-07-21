from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON

from sqlalchemy.orm import declarative_base

from datetime import datetime


Base = declarative_base()


class Investigation(Base):

    __tablename__ = "investigations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String,
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    confidence = Column(
        Integer,
        nullable=False
    )

    report = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )