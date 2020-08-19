"""
The services module of this blueprint.
"""
# pylint: disable=R0903
class UserService:
    """
    The user services is responsible for storing and retrieving the users. This is a mock implementation, as
    user persistense varies over different platforms and implementations.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_user(reference) -> dict:
        """
        Mock implementation of the get_user method.
        :param reference: the FHIR reference of the user.
        :return: a dict with user information.
        """
        return {'reference': reference, 'name': None, 'anonymous': True}
