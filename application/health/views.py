"""
The view objects for this module.
"""
from flask import Blueprint, jsonify


# pylint: disable=W0612
def create_blueprint() -> Blueprint:
    """
    Blueprint init method.
    :return: the Blueprint instance
    """
    blueprint = Blueprint(__name__.split('.')[-2], __name__, static_folder='static')

    @blueprint.route('/health')
    def health():
        """
        The status of the application for health check purposes.
        :return: JSON map of the status.
        """
        return jsonify({'status': 'OK'})

    return blueprint
