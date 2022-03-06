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

# sqlalchemy() imported as db (db = SQLAlchemy())
"""written previously
class Homogeneity(PkModel):
    #__tablename__ = "homogeneities"
    #top_left = Column(db.BigInter())
"""


class Homogeneity:

    __tablename__ = "homogeneities"

    profile_stat_table = db.Table(
                                       name="profile_stat_table", metadata=metadata,
                                       db.Column(name="location", type_=db.Text, nullable=False),
                                       db.Column(name="intensity", type_=db.Float, nullable=False),
                                       db.Column(name="intensity_relative_to_max", type_=db.Float, nullable=False)
                                       )

    max_region_table = db.Table(
                                       name="max_region_table", metadata=metadata,
                                       db.Column(name="nb_pixels", type_=db.Integer, nullable=False),
                                       db.Column(name="center_of_mass", type_=db.ARRAY(Integer), nullable=False),
                                       db.Column(name="max_intensity", type_=db.Integer, nullable=False))

    intensity_plot_data = db.Table(
                                        name="intensity_plot_data", metadata=metadata,
                                        db.Column(name="x_axis_V_seg", type_=db.Float, nullable=False),
                                        db.Column(name="y_axis_V_seg", type_=db.Float, nullable=False),
                                        db.Column(name="x_axis_H_seg", type_=db.Float, nullable=False),
                                        db.Column(name="y_axis_H_seg", type_=db.Float, nullable=False),
                                        db.Column(name="x_axis_diagUD", type_=db.Float, nullable=False),
                                        db.Column(name="y_axis_diagUD", type_=db.Float, nullable=False),
                                        db.Column(name="x_axis_diagDU", type_=db.Float, nullable=False),
                                        db.Column(name="y_axis_diagDU", type_=db.Float, nullable=False))

    # intensity_plot_data = Array
                                        
                                        
    
    
    def image_array(self, path):
        return cm.get_images_from_multi_tiff(path)[0]

    image_array_ = cm.get_images_from_multi_tiff(path)[0]

    def norm_intensity_profile(self,  img=image_array_):
        norm_intensity_profile_ = homo.get_norm_intensity_profile(img)
        return norm_intensity_profile_

    def max_intensity_region_table(self,  img=image_array_):
        max_intensity_region_table_ = homo.get_max_intensity_region_table(img)
        return max_intensity_region_table_

    def intensity_plot(self,  img=image_array_):
        intensity_plot_ = homo.intensity_plot(img)
        return intensity_plot_

    def profile_stat_table(self, img=image_array_):
        profile_stat_table_ = homo.get_profile_statistics_table(img)
        return profile_stat_table_

    


"""
Final attributes :
Homogeneity.intensity_plot
Homogeneity.max_region_table
Homogeneity.norm_intensity_profile
Homogeneity.profile_state_table

missing: microscopy_info_table defined from microscopes folder
"""
