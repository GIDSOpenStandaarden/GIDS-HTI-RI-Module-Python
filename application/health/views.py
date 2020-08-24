#  Copyright (c) 2020 Headease B.V., This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
from flask import Blueprint, jsonify


def create_blueprint() -> Blueprint:
    """
    Blueprint init method.
    :return: the Blueprint instance
    """
    blueprint = Blueprint(__name__.split('.')[-2], __name__, static_folder='static')

    @blueprint.route('/health')
    def health():
        return jsonify({'status': 'OK'})

    return blueprint
