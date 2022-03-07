"""
homogeneity report elements to include inside templates/homogeneity.html
missing:
- specify path to homogeneity_module from MetroloJ-for-python
- path_temp: define path to save-in and load-from png files.
"""

import os
import requests
import tempfile
import logging
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    send_file,
    current_app,
)

from flask_login import login_required, current_use

from metrologist.field_illum.models import Homogeneity

import code.homogeneity_module as homo


@blueprint.route("/")
@login_required
def homogeneity():
    """return all elements of homogeneity report inside homogeneity.html"""

    # define path to save-in and load-from png files.
    path_temp = "/.../"

    # norm_intensity_data_: load .csv, generate and save it as png then load it.
    norm_intensity_data_ = Homogeneity.norm_intensity_data
    homo.get_norm_intensity_profile(norm_intensity_data_, save_path=path_temp)
    norm_intensity_png_path_ = str(path_temp)+"norm_intensity_profile.png"

    # max intensity table
    max_region_table_ = Homogeneity.max_region_table

    # intensity plot_ : load .csv, generate and save it as png then load it.
    intensity_plot_data_ = Homogeneity.intensity_plot_data
    homo.get_intensity_plot(intensity_plot_data_, save_path=path_temp)
    intensity_plot_png_path_ = str(path_temp)+"intensity_plot.png"

    # profile_stat_table_:
    profile_stat_table_ = Homogeneity.profile_stat_table

    return render_template("templates/homogeneity.html",
                           norm_intensity_png_path=norm_intensity_png_path_,
                           max_region_table=max_region_table_,
                           intensity_plot_png_path=intensity_plot_png_path_,
                           profile_stat_table=profile_stat_table_)
