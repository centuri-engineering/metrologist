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
    "microscopes", __name__, url_prefix="/", static_folder="../static"
)


@blueprint.route("/")
@login_required
def microscopes(scope="group"):
    """List microscopes"""
    if scope == "user":
        user_id = current_user.id
        microscopes_ = Microscope.query.filter_by(user_id=user_id)
    elif scope == "group":
        microscopes_ = Microscope.query.filter(
            Microscope.group_id == current_user.group_id
        )
    else:
        microscopes_ = Microscope.query.all()

    return render_template("microscopes/microscopes.html", microscopes=microscopes_)


@blueprint.route("/new")
@login_required
def new_instruments(scope="group"):
    """List microscopes"""
    new_objective_form = NewObjectiveForm()
    new_modality_form = NewModalityForm()
    new_microscope_form = NewMicroscopeForm()

    if new_objective_form.save.data:
        new_objective_form.create()

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
