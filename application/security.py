"""
Package responsible for enforcing security.
"""

from flask import session, abort


class AccessDenied(Exception):
    """
    Error state for access problems to pick up by the app errorhandler(s).
    """
    status_code = 403

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_view(self):
        """
        Render the dict for the JSON view.
        :return:
        """
        data = dict(self.payload or ())
        data['message'] = self.message
        data['code'] = self.status_code
        return data


def require_session_json(function):
    """
    Decorator to check if there is a valid session available. Throws a 403 if no valid session can be found.
    :param function: the wrapped function.
    :return: a wrapping function.
    """

    def wrapper(*args, **kwargs):
        if session.get('task') is None:
            raise AccessDenied('Forbidden', 403)

        return function(*args, **kwargs)

    return wrapper


def require_session_html(function):
    """
    Decorator to check if there is a valid session available. Throws a 403 if no valid session can be found.
    :param function: the wrapped function.
    :return: a wrapping function.
    """

    def wrapper(*args, **kwargs):
        if session.get('task') is None:
            return abort(403, 'Forbidden')

        return function(*args, **kwargs)

    return wrapper
