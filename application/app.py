"""
The create_app function starts up the hti reference implementation.
This function creates an app instance, to refer to this instance and prevent
circular dependencies, make use of:

from flask import current_app

and use current_app to refer to the app instance
"""
import traceback

from flask import Flask, jsonify
from jose.exceptions import JWTClaimsError

from application import hti, spi, user, treatment, health
from application.database import db
from application.security import AccessDenied


def create_app(config=None) -> Flask:
    """
    Main init method that creates and configures the Flask app instance.
    :param config: an optional configuration mapping.
    :return: an app instance
    """
    app = Flask(__name__, instance_relative_config=True)
    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(config)
    if 'APP_SECRET_KEY' in app.config:
        app.secret_key = app.config['APP_SECRET_KEY']
    _, blueprint_spi, _, _, _ = register_blueprints(app)
    register_error_handlers(app, blueprint_spi)
    setup_database(app)

    return app


# pylint: disable=W0612
def register_error_handlers(app, blueprint_spi):
    """
    Register the error handlers on the app and not the blueprint.
    :param app:
    :return:
    """

    @app.errorhandler(403)
    # pylint: disable=W0613
    def error_403(exception):
        # note that we set the 403 status explicitly
        return blueprint_spi.error(403)

    @app.errorhandler(404)
    # pylint: disable=W0613
    def error_404(exception):
        # note that we set the 404 status explicitly
        return blueprint_spi.error(404)

    @app.errorhandler(AccessDenied)
    def handle_access_denied(error):
        response = jsonify(error.to_view())
        response.status_code = error.status_code
        return response

    @app.errorhandler(JWTClaimsError)
    def handle_jwtclaimserror(error: JWTClaimsError):
        traceback.print_exception(JWTClaimsError, error, None)
        return blueprint_spi.error(400)


def setup_database(app: Flask):
    """
    Creates
    :param app: the Flask application instance.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask):
    """
    Method that registers the blueprints.
    :param app: the Flask application instance.
    """
    blueprint_hti = hti.views.create_blueprint()
    app.register_blueprint(blueprint_hti)
    blueprint_spi = spi.views.create_blueprint()
    app.register_blueprint(blueprint_spi)
    blueprint_user = user.views.create_blueprint()
    app.register_blueprint(blueprint_user)
    blueprint_treatment = treatment.views.create_blueprint()
    app.register_blueprint(blueprint_treatment)
    blueprint_health = health.views.create_blueprint()
    app.register_blueprint(blueprint_health)

    return blueprint_hti, blueprint_spi, blueprint_user, blueprint_treatment, blueprint_health
