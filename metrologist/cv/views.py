# -*- coding: utf-8 -*-
"""
cv report elements to include inside
templates/cv/cv.html

Rk: only works on single tiff file.
Missing: make it work with a multi tiff file.
"""

from distutils.command.build import build
from re import L

from flask import Blueprint, render_template
from flask_login import login_required

from pathlib import Path

from metrologist.cv.models import Cv
# from metrologist.upload_image.forms import UploadImage

# from metrologist.metroloj import common
# from metrologist.metroloj import cv as cvm
# if using metroloj pip package
from metroloj import common
from metroloj import cv as cvm

from tempfile import TemporaryDirectory

blueprint = Blueprint(
    "cv", __name__, url_prefix="/cv", static_folder="../static"
)

PARENT1 = Path(__file__).resolve().parents[1]
PARENT2 = Path(__file__).resolve().parents[2]


@blueprint.route("/")


def cv():
    """
    this function generates the cv report elements in
    order to include them on the corresponding web page.
    the generated plots will be saved in a temporary dir.
    """

    # load input image
    single_img_tif = "/cv/examples/homogeneity_ex1.tif"
    multi_img_path = "/cv/examples/cv_comparatif.tif"
    image, nb_images = common.get_images_from_multi_tiff(
        path=str(PARENT1) + multi_img_path,
        nb_img=True
    )

    # dir path for plots
    graph_path_temp = str(PARENT2) + "/assets/img/"
    build_path = "build/img/"

    # get homogeneity report element for input image
    # plots will be saved into graph_path_temp (arg: save_path)
    cv_records = []
    roi_path_list = []
    roi_build_path_list = []

    if nb_images == 1:
        # hist_nbpixels_vs_grayscale: one hist per tif file.
        hist_x, hist_y = cvm.get_hist_data(img=image)
        hist_path = graph_path_temp + "hist.png"
        hist_build_path = build_path + "hist.png"
        cvm.get_hist_nbpixel_vs_grayintensity(image, output_path=hist_path)

        # images with marked roi: save to database and web display
        roi_data = cvm.get_marked_roi_and_label_single_img(image)
        roi_path = graph_path_temp + "0.roi.png"
        roi_build_path = build_path + "0.roi.png"
        cvm.get_marked_roi_and_label_single_img(
            image,
            output_path=roi_path
            )
        roi_path_list.append(roi_path)
        roi_build_path_list.append(roi_build_path)

        # cv_csv global: includes all img in tiff
        cv_csv = cvm.get_cv_table_global(image)

        # define Cv object attributes
        cv_record = Cv(
            hist_x=hist_x,
            hist_y=hist_y,
            roi_data=roi_data,
            cv_table_sd=cv_csv["sd"],
            cv_table_average=cv_csv["average"],
            cv_table_nb_pixels=cv_csv["nb_pixels"],
            cv_table_cv_value=cv_csv["cv"],
            cv_table_relative_to_min=cv_csv["cv_relative_to_min"]
        )
        cv_records.append(cv_record)

    else:
        # global elements
        # hist:
        hist_path = graph_path_temp + "hist.png"
        hist_build_path = build_path + "hist.png"
        cvm.get_hist_nbpixel_vs_grayintensity(image, output_path=hist_path)
        # cv_csv
        cv_csv = cvm.get_cv_table_global(image)
        # img specific elements
        for i, img in enumerate(image):
            # hist_nbpixels_vs_grayscale: one hist per tif file
            hist_x_temp, hist_y_temp = cvm.get_hist_data(img=img, nb_img=1)
            # roi_data_temp
            roi_data_temp = cvm.get_marked_roi_and_label_single_img(img=img)
            roi_path_temp = graph_path_temp + f"{i}.roi.png"
            roi_build_path_temp = build_path + f"{i}.roi.png"
            cvm.get_marked_roi_and_label_single_img(
                img,
                output_path=roi_path_temp
                )
            roi_path_list.append(roi_path_temp)
            roi_build_path_list.append(roi_build_path_temp)

            # how to load multi images from folder ? have diffee

            cv_record = Cv(
                    hist_x=hist_x_temp,
                    hist_y=hist_y_temp,
                    roi_data=roi_data_temp,
                    cv_table_sd=cv_csv["sd"],
                    cv_table_average=cv_csv["average"],
                    cv_table_nb_pixels=cv_csv["nb_pixels"],
                    cv_table_cv_value=cv_csv["cv"],
                    cv_table_relative_to_min=cv_csv["cv_relative_to_min"]
                )
            cv_records.append(cv_record)

    return render_template(
        "cv/cv.html",
        hist_path=hist_build_path,
        cv_records=cv_records,
        roi_path_list=roi_build_path_list,
        cv_csv=cv_csv
    )
