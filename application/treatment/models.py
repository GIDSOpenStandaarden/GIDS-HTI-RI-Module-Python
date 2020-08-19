"""
The model objects for this module.
"""
from dataclasses import dataclass

from application.database import db


# pylint: disable=C0103
@dataclass
class Treatment(db.Model):
    """
    The treatment persistent entity.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(256))
    description = db.Column(db.String(2048))

    def __repr__(self):
        return f'<Treatment {id}>'

    def to_view(self):
        """
        A api representation of this object.
        :return: the api representation of this object as dict.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description}
