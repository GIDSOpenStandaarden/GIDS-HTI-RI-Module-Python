"""
The view objects for this module.
"""
from flask import Blueprint, session, redirect, request, abort
from flask_classful import FlaskView, route

from application.hti.services import hti_launch_service


def create_blueprint() -> Blueprint:
    """
    Blueprint init method.
    :return: the Blueprint instance
    """
    blueprint = Blueprint(__name__.split('.')[-2], __name__)

    # noinspection PyMethodMayBeStatic
    # pylint: disable=R0201
    class HtiView(FlaskView):
        """
        The HTI launch view.
        """

        @route('module_launch', methods=['POST'])
        def post(self):
            """
            HTI launch entrypoint. The HTI launch token is posted on this entrypoint. The main responsibilities for
            an e-Health application is to unpack and validate this token before starting the e-Health offering.
            :return: either a 403 or an redirect to the start view.
            """
            if 'token' in request.values:
                token = request.values['token']
                task = hti_launch_service.launch(token, request.host)
                if task is None:
                    abort(403, "Forbidden")
                session['task'] = task

                return redirect('index.html')

            return abort(400, 'Bad Request, missing token parameter')

    HtiView.register(blueprint, route_base='/')

    return blueprint
