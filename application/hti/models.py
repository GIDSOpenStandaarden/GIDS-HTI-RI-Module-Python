"""
The model objects for this module.
"""
from dataclasses import dataclass

from application.database import db


# pylint: disable=C0103
@dataclass
class JwtId(db.Model):
    """
    The JwtId represents a the persisted JWT identifier.
    """
    id = db.Column(db.String(256), primary_key=True, autoincrement=False)
