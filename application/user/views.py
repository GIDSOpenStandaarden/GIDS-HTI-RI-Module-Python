"""
The views module of this blueprint module.
"""
from flask import Blueprint, session

from application.security import require_session_json
from application.user.services import UserService


# pylint: disable=W0612
def create_blueprint() -> Blueprint:
    """
    Blueprint init method.
    :return: the Blueprint instance
    """
    blueprint = Blueprint(__name__.split('.')[-2], __name__)

    user_service = UserService()

    @blueprint.route('/api/user/current')
    @require_session_json
    def current():
        """
        Shows the current user, stored in the session
        :return:
        """
        task = session.get('task')
        for_user = task['for']['reference']
        return user_service.get_user(for_user)

    return blueprint
