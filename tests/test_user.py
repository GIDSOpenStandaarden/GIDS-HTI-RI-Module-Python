from flask.testing import FlaskClient

from tests.conftest import AuthActions


def test_current(client: FlaskClient, auth: AuthActions):
    response = client.get('/api/user/current')

    assert response.status_code == 403

    auth.login()

    response = client.get('/api/user/current')
    assert response.status_code == 200
    assert response.json['reference'] == 'Person/fa1636df'
