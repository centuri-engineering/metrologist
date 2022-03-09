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

import homogeneity_module as homo
import common_module as cm

"""
sqlalchemy() imported as db (db = SQLAlchemy())
when imported metrologist.database
"""

metadata = db.MetaData()

"""
Rk: missing: microscopy_info_table defined from microscopes folder
as it's supposed to be part of "microscopes" dir rather than
homogeneity. 
"""


class Homogeneity(PkModel):
    """
    Homogeneity class refers to homogeneity report generating
    from a given image:
        1. norm_intensity_data: np.array used to generate the normalized
        intensity profile of the image. It's used to generate the corresponding
        image.
        2. max_region_table: dataframe enclosing information about the max
        intensity area of the given image.
        3. intensity_plot_data: np.array used to generate the intensity plot of
        the mid horizontal, mid vertical and the two diagonal lines of the image.
        4. profile_stat_table: dataframe showing the intensity values of 9
        specific pixels and their ratio over the maximum intensity value of
        the array.
    """

    __tablename__ = "homogeneities"

    # user_id
    user_id = Column(db.ForeignKey("users.id"), nullable=False)

    # microscope
    microscope_id = Column(db.ForeignKey("microscopes.id"), nullable=False)

    # datetime
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)

    # max_region_table
    max_region_table_nb_pixels = Column(db.Integer, nullable=False)
    max_region_table_center_of_mass = Column(db.ARRAY(Integer), nullable=False)
    max_region_table_max_intensity = Column(db.Integer, nullable=False)

    # intensity_plot_data
    intensity_plot_data_x_axis_V_seg = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_y_axis_V_seg = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_x_axis_H_seg = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_y_axis_H_seg = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_x_axis_diagUD = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_y_axis_diagUD = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_x_axis_diagDU = Column(db.ARRAY(Float), nullable=False)
    intensity_plot_data_y_axis_diagDU = Column(db.ARRAY(Float), nullable=False)

    # profile_stat_table 
    profile_stat_table_location = Column(db.String(128), nullable=False)
    profile_stat_table_intensity = Column(db.Float, nullable=False)
    profile_stat_table_intensity_relative_to_max = Column(db.Float, nullable=False)

    
    # norm_intensity_data
    norm_intensity_data = Column(db.ARRAY(Float, dimensions=2)) 
