# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import logging

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from metrologist.extensions import login_manager, ldap_manager, omero_manager
from metrologist.public.forms import LoginForm
from metrologist.user.models import User, Group
from metrologist.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")

log = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@omero_manager.save_user
def save_user_omero(user_info):

    username = user_info["username"]
    name = user_info.get("fullname", "").split()
    first = last = None
    if len(name) > 1:
        first = name[0]
        last = " ".join(name[1:])
    elif len(name) == 1:
        last = username

    groupname = user_info.get("groupname", "default")
    groups = Group.query.filter_by(groupname=groupname)
    if groups.first():
        group = groups.first()
        current_app.logger.info("Found group %s", groupname)
    else:
        group = Group.create(
            groupname=groupname,
            active=True,
        )
        current_app.logger.info("Created group %s", groupname)

    is_admin = user_info.get("is_admin", False)
    existing = User.query.filter_by(username=username).first()
    if existing:
        log.warning(
            "User %s is already registered, updating db with current info", username
        )
        existing.update(
            first_name=first,
            last_name=last,
            active=True,
            group_id=group.id,
            is_admin=is_admin,
        )
        return existing

    user = User.create(
        username=username,
        first_name=first,
        last_name=last,
        active=True,
        group_id=group.id,
        is_admin=is_admin,
    )

    return user


@ldap_manager.save_user
def save_user_ldap(dn, username, user_info, memberships):
    """Saves a user that managed to log in with LDAP

    Group determination method is based on the first 'OU=' section
    in the user DN, might need tweaking
    """
    existing = User.query.filter_by(username=username).first()
    if existing:
        log.warning("User %s is already registered", username)
        return existing

    name = user_info.get("cn", "").split()

    first = last = None
    if len(name) > 1:
        first = name[0]
        last = " ".join(name[1:])
    elif len(name) == 1:
        last = username

    groupname = None
    for sec in dn.split(","):
        if sec.startswith("OU"):
            groupname = sec.split("=")[1]
            break
    else:
        groupname = "default"

    groups = Group.query.filter_by(groupname=groupname)
    if groups.first():
        group = groups.first()
        current_app.logger.info("Found group %s", groupname)
    else:
        group = Group.create(
            groupname=groupname,
            active=True,
        )
        current_app.logger.info("Created group %s", groupname)

    user = User.create(
        username=username,
        first_name=first,
        last_name=last,
        active=True,
        group_id=group.id,
    )

    return user


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            if form.user:
                login_user(form.user)
            else:
                user = User.query.filter_by(username=form.username.data).first()
                login_user(form.user)

            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
