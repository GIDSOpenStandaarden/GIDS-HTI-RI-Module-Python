"""
Configuration file for the HTI reference implementation application.
"""
import os
import uuid


def envget_str(key: str, dflt: str) -> str:
    """
    Gets a value from the os.environ, and defaults to the value of dflt if not set in the environment.
    :param key: environment variable name
    :param dflt: default value, if not present in the environment
    :return: either the value of the environment variable or the default value (dflt)
    """
    return os.environ[key] if key in os.environ else dflt


def envget_bool(key, dflt: bool) -> bool:
    """
    Gets a value from the os.environ, and defaults to the value of dflt if not set in the environment.
    :param key: environment variable name
    :param dflt: default value, if not present in the environment
    :return: either the value of the environment variable or the default value (dflt)
    """
    val = envget_str(key, 'True' if dflt else 'False')
    return val.lower() in ['true', 'yes', '1', 'y']


DEBUG = envget_bool('DEBUG', False)
SQLALCHEMY_TRACK_MODIFICATIONS = envget_bool('SQLALCHEMY_TRACK_MODIFICATIONS', False)
SQLALCHEMY_ECHO = envget_bool('SQLALCHEMY_ECHO', False)

APP_SECRET_KEY = envget_str('APP_SECRET_KEY', str(uuid.uuid1()))
HTI_ALLOWED_PORTALS = envget_str('HTI_ALLOWED_PORTALS',
                                 'localhost:8080, gids-hti-ri-portal-java.edia-tst.eu, gids-hti-portal.edia-tst.eu')
SQLALCHEMY_DATABASE_URI = envget_str('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
