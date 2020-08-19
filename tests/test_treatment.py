from flask.testing import FlaskClient

from tests.conftest import AuthActions


def test_current(client: FlaskClient, auth: AuthActions):
    response = client.get('/api/treatment/current')

    assert response.status_code == 403

    auth.login()

    response = client.get('/api/treatment/current')
    assert response.status_code == 200
    assert response.json['id'] == 2


def test_all(client: FlaskClient, auth: AuthActions):
    response = client.get('/api/treatment/all')

    assert response.status_code == 403

    auth.login()

    response = client.get('/api/treatment/all')
    assert response.status_code == 200
    assert len(response.json['treatments']) == 4
