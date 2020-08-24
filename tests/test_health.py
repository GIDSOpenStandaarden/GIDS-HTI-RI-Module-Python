from flask.testing import FlaskClient

from tests.conftest import AuthActions


def test_index(client: FlaskClient, auth: AuthActions):
    response = client.get("/health")
    assert response.status_code == 200

    assert response.json['status'] == 'OK'
