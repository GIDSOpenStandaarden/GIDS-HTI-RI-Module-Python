"""
The view objects for this module.
"""
from flask import Blueprint, session, abort
from flask_classful import FlaskView

from application.security import require_session_json
from application.treatment.services import TreatmentService


def create_blueprint():
    """
    Blueprint init method.
    :return: the Blueprint instance
    """
    blueprint = Blueprint(__name__.split('.')[-2], __name__)
    treatment_service = TreatmentService()

    # noinspection PyMethodMayBeStatic
    # pylint: disable=R0201
    class TreatmentView(FlaskView):
        """
        The implementation of the /api/treatment API segment.
        """

        @require_session_json
        def get(self, treatment_id: int):
            """
            Gets a treatment by id
            :param treatment_id:
            :return: a treatment, else 404
            """
            treatment = treatment_service.get_treatment(treatment_id)
            return treatment.to_view() if treatment is not None else abort(404)

        @require_session_json
        def all(self):
            """
            Gets all treatments.
            :return: all treatments.
            """
            return {'treatments': [treatment.to_view() for treatment in treatment_service.get_all_treatments()]}

        @require_session_json
        def current(self):
            """
            Gets the current treatment from the FHIR task from the HTI launch object.
            :return: the current treatment from the FHIR task from the HTI launch object.
            """
            task = session.get('task')
            definition_reference: str = task['definitionReference']['reference']
            task_id = definition_reference.split('ActivityDefinition/')[1]
            if task_id is not None:
                treatment = treatment_service.get_treatment(int(task_id))
                return treatment.to_view() if treatment is not None else abort(404)
            return abort(404)

    TreatmentView.register(blueprint, route_base='/api/treatment', trailing_slash=False)

    return blueprint
