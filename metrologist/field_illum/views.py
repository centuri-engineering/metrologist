# -*- coding: utf-8 -*-
"""
homogeneity report elements to include inside
templates/homogeneities/homogeneity.html
"""

from flask import Blueprint, render_template
from flask_login import login_required

from metrologist.field_illum.models import Homogeneity
# from metrologist.upload_image.forms import UploadImage

from metrologist.metroloj import common, homo
from tempfile import TemporaryDirectory

blueprint = Blueprint(
    "field_illum", __name__, url_prefix="/field_illum", static_folder="../static"
)


@blueprint.route("/")
@login_required
def field_illum():
    """
    this function generates the homogeneity report elements on the input image in
    order to include them on the corresponding web page.
    the generated plots will be saved in a temporary dir.
    """

    # load input image
    image = common.get_images_from_multi_tiff(
        path="/examples/homogeneity_ex1.tif",
        single=True
        )
 
    # temp path for plots
    graph_path_temp = TemporaryDirectory()
    intensity_plot_path = graph_path_temp + "intensity_plot.png"
    norm_intensity_profile_path = graph_path_temp + "norm_intensity_profile.png"

    # get homogeneity report element for input image
    # plots will be saved into graph_path_temp (arg: save_path)
 
    max_region_info  = homo.get_max_intensity_region(image)

    profile_stat_table = homo.get_profile_statistics_table(image)

    _ , intensity_plot_data = homo.get_intensity_plot(
        image,
        save_path=graph_path_temp
        )

    norm_intensity_matrix = homo.get_norm_intensity_matrix(image)
    homo.get_norm_intensity_profile(
        image,
        save_path=graph_path_temp
        )

    # define Homogeneity object attributes 

    homogeneity_record = Homogeneity(
        max_region_table_nb_pixels = max_region_info["nb pixels"],
        max_region_table_center_of_mass = max_region_info["center of mass"],
        max_region_table_max_intensity = max_region_info["max intensity"],
        profile_stat_table_location = profile_stat_table["location"],
        profile_stat_table_intensity = profile_stat_table["intensity"],
        profile_stat_table_intensity_relative_to_max = profile_stat_table["intensity relative to max"],
        intensity_plot_data_x_axis_V_seg = intensity_plot_data["x_axis_V_seg"],
        intensity_plot_data_y_axis_V_seg = intensity_plot_data["y_axis_V_seg"],
        intensity_plot_data_x_axis_H_seg = intensity_plot_data["x_axis_H_seg"],
        intensity_plot_data_y_axis_H_seg = intensity_plot_data["y_axis_H_seg"],
        intensity_plot_data_x_axis_diagUD = intensity_plot_data["x_axis_diagUD"],
        intensity_plot_data_y_axis_diagUD = intensity_plot_data["y_axis_diagUD"],
        intensity_plot_data_x_axis_diagDU = intensity_plot_data["x_axis_diagDU"],
        intensity_plot_data_y_axis_diagDU = intensity_plot_data["y_axis_diagDU"],
        norm_intensity_data = norm_intensity_matrix
        )

    return render_template(
        "field_illum/field_illum.html",
        homogeneity_record=homogeneity_record,
        intensity_plot_path=intensity_plot_path,
        norm_intensity_profile_path=norm_intensity_profile_path
        )
