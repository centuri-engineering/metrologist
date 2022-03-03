import homogeneity_module as homo
import common_module as cm


"""written previously
class Homogeneity(PkModel):
    #__tablename__ = "homogeneities"
    #top_left = Column(db.BigInter())
"""


class Homogeneity:

    def __init__ (self, path):
        self.path = path

    def image_array(self, path):
        return cm.get_images_from_multi_tiff(path)[0]

    image_array = cm.get_images_from_multi_tiff(path)[0]

    def norm_intensity_profile(self,  img=image_array):
        norm_intensity_profile_ = homo.get_norm_intensity_profile(img)
        return norm_intensity_profile_

    def max_intensity_region_table(self,  img=image_array):
        max_intensity_region_table_ = homo.get_max_intensity_region_table(img)
        return max_intensity_region_table_

    def intensity_plot(self,  img=image_array):
        intensity_plot_ = homo.intensity_plot(img)
        return intensity_plot_

    def profile_stat_table(self, img=image_array):
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
