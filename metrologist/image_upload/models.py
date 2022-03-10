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


class Image(PkModel):

    __tablename__ = "images"
    created_at = Column(db.DateTime, nullable=True)
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref=__tablename__)
    path = Column(db.String(), nullable=False)
