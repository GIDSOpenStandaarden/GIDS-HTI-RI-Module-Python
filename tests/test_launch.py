import json
from datetime import datetime, timedelta
from uuid import uuid1

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from flask.testing import FlaskClient
from jose import jwt, jwk
from jose.constants import ALGORITHMS
from pytest_mock import MockFixture


def test_launch_error(client: FlaskClient):
    response = client.post('/module_launch', data={'token': None})
    assert response.status_code == 400


def test_launch(client: FlaskClient, mocker: MockFixture):
    ## urllib.request.urlopen
    key_pair = RSA.generate(2048)
    private_key = key_pair.export_key()
    pair_publickey: RsaKey = key_pair.publickey()
    public_key = pair_publickey.export_key()
    kid = str(uuid1())

    def urlopen(url):
        key = jwk.construct(public_key, ALGORITHMS.RS512).to_dict()
        key['kid'] = kid
        data = json.dumps({'keys': [key]}).encode('UTF8')

        class Stream:
            def read(self):
                return data

        return Stream()

    mocker.patch('application.hti.services.urlopen', new=urlopen)

    task = {
        "resourceType": "Task",
        "id": "8c83a9ae",
        "definitionReference": {
            "reference": "ActivityDefinition/2"
        },
        "status": "requested",
        "intent": "plan",
        "for": {
            "reference": "Person/fa1636df"
        }
    }
    token = jwt.encode({'iss': 'https://localhost:8080',
                        'aud': 'localhost',
                        'jti': str(uuid1()),
                        'exp': datetime.utcnow() + timedelta(seconds=30),
                        'task': task}, private_key, algorithm=ALGORITHMS.RS512, headers={'kid': kid})
    response = client.post('/module_launch', data={'token': token})
    assert response.status_code == 302

    ## Replay
    response = client.post('/module_launch', data={'token': token})
    assert response.status_code == 400
