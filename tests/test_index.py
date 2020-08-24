from flask.testing import FlaskClient

from tests.conftest import AuthActions


def test_index(client: FlaskClient, auth: AuthActions):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/index.html'

    response = client.get('index.html')

    print(response)
    assert response.status_code == 403

    auth.login()

    response = client.get('index.html')

    print(response)
    assert response.status_code == 200


def test_error_pages(client: FlaskClient):
    response = client.get("/dasd")
    assert response.status_code == 404
