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

    norm_intensity_data = db.Table("norm_intensity_data", metadata=metadata)

    max_region_table = db.Table(
        name="max_region_table", metadata=metadata,
        db.Column(name="nb_pixels", type_=db.Integer, nullable=False),
        db.Column(name="center_of_mass", type_=db.ARRAY(Integer), nullable=False),
        db.Column(name="max_intensity", type_=db.Integer, nullable=False)
        )

    intensity_plot_data = db.Table(
        name="intensity_plot_data", metadata=metadata,
        db.Column(name="x_axis_V_seg", type_=db.Float, nullable=False),
        db.Column(name="y_axis_V_seg", type_=db.Float, nullable=False),
        db.Column(name="x_axis_H_seg", type_=db.Float, nullable=False),
        db.Column(name="y_axis_H_seg", type_=db.Float, nullable=False),
        db.Column(name="x_axis_diagUD", type_=db.Float, nullable=False),
        db.Column(name="y_axis_diagUD", type_=db.Float, nullable=False),
        db.Column(name="x_axis_diagDU", type_=db.Float, nullable=False),
        db.Column(name="y_axis_diagDU", type_=db.Float, nullable=False)
        )

    profile_stat_table = db.Table(
        name="profile_stat_table", metadata=metadata,
        db.Column(name="location", type_=db.Text, nullable=False),
        db.Column(name="intensity", type_=db.Float, nullable=False),
        db.Column(name="intensity_relative_to_max", type_=db.Float, nullable=False)
        )
