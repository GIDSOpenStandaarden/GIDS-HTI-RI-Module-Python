from flask.testing import FlaskClient


def test_index(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/index.html'

    response = client.get('index.html')

    print(response)
    assert response.status_code == 200


def test_error_pages(client: FlaskClient):
    response = client.get("/dasd")
    assert response.status_code == 404
