# -*- coding: utf-8 -*-
"""Public forms."""
import logging

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired
from flask_ldap3_login import AuthenticationResponseStatus

from metrologist.user.models import User
from metrologist.extensions import auth_manager
from metrologist.omero_login import OmeroLoginManager

log = logging.getLogger(__name__)


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super().validate()

        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()

        if isinstance(auth_manager, OmeroLoginManager):
            response = auth_manager.authenticate(self.username.data, self.password.data)
            if response.status == AuthenticationResponseStatus.fail:
                self.username.errors.append(
                    f"User {self.username.data} is not known to OMERO"
                )
                return False

            elif response.status == AuthenticationResponseStatus.success:
                auth_manager._save_user(response.user_info)
                return True

        elif auth_manager is not None:
            response = auth_manager.authenticate(self.username.data, self.password.data)
            if response.status == AuthenticationResponseStatus.success:
                log.info("Logged in through %s", auth_manager.__class__.__name__)
                return True

        # Fallback to local authentication
        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True
