# -*- coding: utf-8 -*-
"""annotation views."""
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

from flask_login import login_required, current_user

from metrologist.microscopes.models import Microscope, Objective, Modality
from metrologist.microscopes.forms import (
    NewObjectiveForm,
    NewModalityForm,
    NewMicroscopeForm,
)


blueprint = Blueprint(
    "microscopes", __name__, url_prefix="/microscopes", static_folder="../static"
)


@blueprint.route("/")
@login_required
def microscopes():
    """List microscopes"""
    microscopes = Microscope.query.all()

    return render_template("microscopes/microscopes.html", microscopes=microscopes)


@blueprint.route("/new", methods=["GET", "POST"])
@login_required
def new_instruments(scope="group"):
    """List microscopes"""
    new_objective_form = NewObjectiveForm()
    new_modality_form = NewModalityForm()
    new_microscope_form = NewMicroscopeForm()

    if new_objective_form.validate_on_submit():
        new_objective_form.create()
        flash("New objective created", "success")
        return render_template(
            "microscopes/new.html",
            new_objective_form=NewObjectiveForm(),
            new_modality_form=new_modality_form,
            new_microscope_form=new_microscope_form,
        )

    if new_modality_form.save.data:
        new_modality_form.create()

    if new_microscope_form.save.data:
        new_microscope_form.create()

    return render_template(
        "microscopes/new.html",
        new_objective_form=new_objective_form,
        new_modality_form=new_modality_form,
        new_microscope_form=new_microscope_form,
    )
