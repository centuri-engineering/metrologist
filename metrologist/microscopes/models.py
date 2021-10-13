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
instrument_objectives = db.Table(
    "instrument_objectives",
    db.Model.metadata,
    Column("instrument_id", db.Integer, db.ForeignKey("instruments.id")),
    Column("objective_id", db.Integer, db.ForeignKey("objectives.id")),
)


class Instrument(PkModel):
    """A combination of a microscope and a collection of objectives

    This is in accordance (but with less info for now) with the omero schema
    An objective can be used on multiple instruments.
    """

    __tablename__ = "intruments"
    microscope_id = reference_col("microscopes", nullable=False)
    microscope = relationship("Microscope", backerf=__tablename__)
    objectives = relationship("Objective", secondary=instrument_objectives)
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)


class Microscope(PkModel):
    """The 'naked' statif"""

    __tablename__ = "microscopes"
    name = Column(db.String(128), nullable=False)
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    # Bright field, confocal etc
    modality_id = reference_col("modalities", nullable=False)
    modality = relationship("Modality", backerf=__tablename__)


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
