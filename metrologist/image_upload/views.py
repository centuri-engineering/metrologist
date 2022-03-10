"""annotation views."""
import os
import io
import requests
import tempfile
import logging
from datetime import datetime
from pathlib import Path

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
from metrologist.image_upload.models import Image

from metrologist.image_upload.forms import ImageForm

data_path = (Path(os.environ.get("DATA_PATH", ".")) / "images").resolve()
if not data_path.exists():
    data_path.mkdir(mode=511, parents=True)

log = logging.getLogger(__name__)

blueprint = Blueprint(
    "image_upload", __name__, url_prefix="/image_upload", static_folder="../static"
)


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def upload_image():
    """perform image upload and register it in the DB"""
    form = ImageForm()
    if form.validate_on_submit():
        log.info(form.image)
        log.info(request.files)
        storage = request.files["image"]

        fname = (
            data_path
            / current_user.username
            / storage.filename.replace(" ", "_").strip()
        )
        if not fname.parent().exists():
            fname.parent().mkdir()
        storage.save(fname)
        image = Image(created_at=datetime.utcnow(), user_id=current_user.id, path=fname)

    return render_template("image_upload/image_upload.html", form=form)
