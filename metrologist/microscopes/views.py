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

from metrologist.microscope.models import Microscope, Objective, Modality

from metrologist.microscope.forms import NewObjectiveForm
