"""User models."""

"""
Rk: only works on single tiff file. 
Missing: make it work with a multi tiff file.
"""

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
sqlalchemy() imported as db (db = SQLAlchemy())
when imported metrologist.database
"""

metadata = db.MetaData()

"""
Rk: missing: microscopy_info_table defined from microscopes folder
as it's supposed to be part of "microscopes" dir rather than
cv. 
"""

class Cv(PkModel):
    """
    """

    __tablename__ = "cv"

   # user_id
    user_id = Column(db.ForeignKey("users.id"), nullable=False)

    # microscope
    microscope_id = Column(db.ForeignKey("microscopes.id"), nullable=False)

    # datetime
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)

    # hist_nbpixels_vs_grayscale
    hist_x = Column(db.ARRAY(db.Float), nullable=False)
    hist_y = Column(db.ARRAY(db.Float), nullable=False)

    # images with marked roi and label: stored as numpy arrays
    roi_data = Column(db.ARRAY(db.Float), nullable=False)

    """for mutli tiff file: trial
    # hist_nbpixels_vs_grayscale
    for i in range(nb_images):
        index_i = i+1
        colname_x, colname_y = f"hist_x_{index_i}", f"hist_y_{index_i}"
        exec(f"{colname_x}=db.Column(db.ARRAY(Float), nullable=False)")
        exec(f"{colname_y}=db.Column(db.ARRAY(Float), nullable=False)")
    
    # images with marked roi and label: stored as numpy arrays
    for j in range(nb_images):
        index_j = j+1
        colname = f"roi_data_{index_j}"
        exec(f"{colname}=db.Column(db.ARRAY(Float), nullable=False)")
    """

    # cv_table
    cv_table_sd = Column(db.Float(), nullable=False)
    cv_table_average = Column(db.Float(), nullable=False)
    cv_table_nb_pixels = Column(db.Float(), nullable=False)
    cv_table_cv_value = Column(db.Float(), nullable=False)
    cv_table_relative_to_min = Column(db.Float(), nullable=False)
