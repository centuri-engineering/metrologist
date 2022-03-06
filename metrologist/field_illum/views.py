"""
homogeneity report elements to include inside templates/homogeneity.html
"""
from flask import Blueprint, render_template

@blueprint.route("/")
def homogeneity(path):
    """ return all elements of homogeneity report inside homogeneity.html """
    
    homo_elements = Homogeneity(path)

    intensity_plot = Homogeneity.intensity_plot
    norm_intensity_profile = Homogeneity.norm_intensity_profile
    max_region_table = Homogeneity.max_region_table
    microscopy_info_table = Homogeneity.microscopy_info_table
    profile_state_table = Homogeneity.profile_state_table

    return render_template("homogeneity.html",
                                                intensity_plot=intensity_plot,
                                                norm_intensity_profile=norm_intensity_profile,
                                                max_region_table=max_region_table,
                                                microscopy_info_table=microscopy_info_table,
                                                profile_state_table=profile_state_table)
