"""Use an omero server to authenticate user and gather group info

This is heaviliy inspired by https://flask-ldap3-login.readthedocs.io/
"""
import logging
from enum import Enum

from flask_ldap3_login import AuthenticationResponseStatus
log = logging.getLogger(__name__)


try:
    import omero
    from omero.gateway import BlitzGateway
except ImportError:
    log.info("omero module not found, this will not work")



class AuthenticationResponse:
    """
    A response object when authenticating. Lets us pass status codes around
    and also user data.

    Args:
        status (AuthenticationResponseStatus):  The status of the result.
        user_info (dict): User info dictionary obtained from omero.
    """

    # From flask-ldap3-login, thanks

    def __init__(
        self,
        status=AuthenticationResponseStatus.fail,
        user_info=None,
    ):
        self.user_info = user_info
        self.status = status


class OmeroLoginManager:
    def __init__(self, app=None):

        self.app = app
        self.config = {}
        self._save_user = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Configures this extension with the given app. This registers a
        ``teardown_appcontext`` call, and attaches this ``OmeroLoginManager``
        to it as ``app.omero_login_manager``.

        Args:
            app (flask.Flask): The flask app to initialise with
        """
        app.omero_login_manager = self
        self.init_config(app.config)

    def init_config(self, config):
        """
        Configures this extension with a given configuration dictionary.
        This allows use of this extension without a flask app.

        Args:
            config (dict): A dictionary with configuration keys
        """
        self.config.update(config)
        self.config.setdefault("OMERO_PORT", 4064)
        self.config.setdefault("OMERO_HOST", "localhost")
        log.info(
            "Setting omero host to %s:%d",
            self.config["OMERO_HOST"],
            self.config["OMERO_PORT"],
        )

    def authenticate(self, username, password):

        client = omero.client(
            host=self.config["OMERO_HOST"], port=self.config["OMERO_PORT"]
        )
        session = client.createSession(username, password)
        with BlitzGateway(client_obj=client) as conn:
            if conn.isConnected():
                log.info("succesfully connected to OMERO")
                response = AuthenticationResponse(
                    status=AuthenticationResponseStatus.success,
                    user_info=self.get_user_info(conn),
                )
            else:
                response = AuthenticationResponse(
                    status=AuthenticationResponseStatus.fail, user_info={}
                )
        return response

    def get_user_info(self, conn):
        user = conn.getUser()
        info = {
            "username": user.getName(),
            "fullname": user.getFullName(),
            "groupname": conn.getGroupFromContext().getName(),
            "groups": [g.getName() for g in conn.getGroupsMemberOf()],
            # Check if you are an Administrator
            "is_admin": conn.isAdmin(),
            "is_full_admin": conn.isFullAdmin(),
            "privileges": conn.getCurrentAdminPrivileges(),
        }
        log.info("Found user info: %s", info)
        if conn.isAdmin():
            log.warning("Created admin user")
        return info

    def save_user(self, callback):
        """
        This sets the callback for saving a user that has been looked up from
        from ldap.

        The function you set should take a user dn (unicode), username
        (unicode) and userdata (dict), and memberships (list).

        ::

            @ldap3_manager.save_user
            def save_user(dn, username, userdata, memberships):
                return User(username=username, data=userdata)

        Your callback function MUST return the user object in your ORM
        (or similar). as this is used within the LoginForm and placed
        at ``form.user``

        Args:
            callback (function): The function to be used as the save user
                                 callback.
        """

        self._save_user = callback
        return callback
