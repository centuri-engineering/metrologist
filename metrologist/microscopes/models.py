# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
import logging


from metrologist.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
)

log = logging.getLogger(__name__)

"""
Many to Many relation between intruments and objectives
"""


microscope_objectives = db.Table(
    "microscope_objectives",
    db.Model.metadata,
    Column("microscope_id", db.Integer, db.ForeignKey("microscopes.id")),
    Column("objective_id", db.Integer, db.ForeignKey("objectives.id")),
)


class Microscope(PkModel):
    """The 'naked' statif"""

    __tablename__ = "microscopes"
    name = Column(db.String(128), nullable=False)
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    # Bright field, confocal etc
    modality_id = reference_col("modalities", nullable=False)
    modality = relationship("Modality", backref=__tablename__)
    objectives = relationship("Objective", secondary=microscope_objectives)
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    vendor = Column(db.String(128), nullable=False)


class Objective(PkModel):
    __tablename__ = "objectives"
    name = Column(db.String(128), nullable=False)
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    lensNA = Column(db.Float(), nullable=True)
    magnification = Column(db.Integer(), nullable=True)


class Modality(PkModel):
    __tablename__ = "modalities"
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    name = Column(db.String(128), nullable=False)
