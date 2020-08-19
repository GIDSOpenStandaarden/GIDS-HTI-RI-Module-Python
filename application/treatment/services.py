"""
The services module of this blueprint.
"""
import os
import typing

import yaml
from flask import current_app
from yaml import BaseLoader

from application.database import db
from application.treatment.models import Treatment


def _require_init(function: typing.Callable):
    """
    Decorator for calling the init function.
    :return: the wrapper.
    """

    def wrapper(self, *args, **kwargs):
        if not self.initialized:
            self.init()
        return function(self, *args, **kwargs)

    return wrapper


class TreatmentService:
    """
    The service responsible for managing the treatments in this module.
    """

    def __init__(self, yaml_file='treatments.yaml'):
        self.initialized = False
        self.yaml_file = yaml_file

    def init(self):
        """
        Initializes the treatments from the provided YAML file and synchronizes them with the database.
        """
        resource_path = os.path.join(os.path.split(__file__)[0], "resources")
        with open(f'{resource_path}/{self.yaml_file}', 'rt') as file, current_app.app_context():
            treatments = yaml.load(file, Loader=BaseLoader)
            with current_app.app_context():
                for treatment in treatments['treatments']:
                    treatment_id = int(treatment['id'])
                    existing_treatment = Treatment.query.get(treatment_id)
                    if existing_treatment is None:
                        new_treatment = Treatment(id=treatment_id, name=treatment['name'],
                                                  description=treatment['description'])
                        db.session.add(new_treatment)
                    else:
                        existing_treatment.name = treatment['name']
                        existing_treatment.description = treatment['description']
                db.session.commit()
        self.initialized = True

    # pylint: disable=R0201
    @_require_init
    def get_all_treatments(self) -> typing.List[Treatment]:
        """
        Gets all the treatments in the database.
        :return:
        """
        # if not self.initialized:
        #     self.init()
        with current_app.app_context():
            return Treatment.query.all()

    # pylint: disable=R0201
    @_require_init
    def get_treatment(self, treatment_id: int) -> Treatment:
        """
        Gets a treatment by id.
        :param treatment_id: the treatment id
        :return: a treatment found with the id, or none.
        """
        # if not self.initialized:
        #     self.init()

        with current_app.app_context():
            return Treatment.query.get(treatment_id)
