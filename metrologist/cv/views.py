# -*- coding: utf-8 -*-
"""
cv report elements to include inside
templates/cv/cv.html

Rk: only works on single tiff file. 
Missing: make it work with a multi tiff file.
"""

from re import L

from flask import Blueprint, render_template
from flask_login import login_required

from metrologist.cv.models import Cv
# from metrologist.upload_image.forms import UploadImage

from metrologist.metroloj import common, cv
from tempfile import TemporaryDirectory

blueprint = Blueprint(
    "cv", __name__, url_prefix="/cv", static_folder="../static"
)


@blueprint.route("/")

def cv():
    """
    this function generates the cv report elements in
    order to include them on the corresponding web page.
    the generated plots will be saved in a temporary dir.
    """

    # load input image
    image, nb_images = common.get_images_from_multi_tiff(
        path="/examples/homogeneity_ex1.tif",
        zdim=True
    )

    # temp path for plots
    graph_path_temp = TemporaryDirectory()
    hist_path = graph_path_temp + "hist.png"
    roi_path = graph_path_temp + "0.roi.png"
    

    # get homogeneity report element for input image
    # plots will be saved into graph_path_temp (arg: save_path)

    # hist_nbpixels_vs_grayscale
    hist_x, hist_y = cv.get_hist_data(img=image, nb_img=nb_images)
    cv.get_hist_nbpixel_vs_grayintensity(image, output_dir=hist_path)

    # images with marked roi
    roi_data_0 = cv.get_marked_roi_and_label_single_img(image)
    cv.get_marked_roi_and_label_single_img(
        image,
        output_dir=graph_path_temp
        )

    # cv.csv as a dict
    cv_csv = cv.get_cv_table_global(image)

    # define Cv object attributes
    cv_record = Cv(
        hist_x_0 = hist_x,
        hist_y_0 = hist_y,
        roi_data_0 = roi_data_0,
        cv_table_sd = cv_csv["sd"],
        cv_table_average = cv_csv["average"],
        cv_table_nb_pixels = cv_csv["nb_pixels"],
        cv_table_cv_value = cv_csv["cv"],
        cv_table_relative_to_min = cv_csv["cv_relative_to_min"]
    )

    return render_template(
        "cv/cv.html",
        cv_record = cv_record,
        hist_path = hist_path,
        roi_path = roi_path,
        cv_csv = cv_csv
    )