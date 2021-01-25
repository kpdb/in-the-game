import time
from datetime import datetime

import jwt
import pytest

from in_the_game.auth import repository, models
from in_the_game.auth.handlers import decode_token, sign_with_token


def test_sign_with_jwt_token():
    test_id = 'some_test_id'

    token_response = sign_with_token(test_id)

    decoded_payload = jwt.decode(token_response, 'secret', algorithms=['HS256'])
    assert 'expires' in decoded_payload
    assert decoded_payload['user_id'] == test_id


def test_decode_jwt_token():
    payload = {"user_id": "abc123", "expires": time.time() + 600}
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    decoded_payload = decode_token(token)
    assert decoded_payload == payload


@pytest.mark.parametrize(
    "token",
    [
        {},
        {'user_id': 'aaa'},
        {'user_id': 'aaa', 'expires': None},
        {'user_id': 'aaa', 'expires': time.time() - 600}
    ]
)
def test_decode_assume_token_expired(token):
    assert decode_token(token) == {}


def test_user_login(test_app, monkeypatch):
    test_login_data = {
        "email": "aaa@bbb.pl",
        "password": "aaa_bbb_pl",
    }
    test_login_request = models.UserLogin(**test_login_data)

    async def mock_get_user_by_email(user_email):
        return {
            "email": user_email,
            "password": 'aaa_bbb_pl',
            "created_at": datetime.now(),
            "modified_at": None,
        }

    monkeypatch.setattr(repository, "get_user_by_email", mock_get_user_by_email)

    response = test_app.post("/auth/login", data=test_login_request.json())
    assert response.status_code == 201

    access_token = response.json()['access_token']
    assert access_token

    decoded_payload = decode_token(access_token)
    assert decoded_payload['user_id'] == test_login_data['email']


def test_user_login_fails_when_user_doesnt_exist(test_app, monkeypatch):
    test_login_data = {
        "email": "aaa@bbb.pl",
        "password": "aaa_bbb_pl",
    }
    test_login_request = models.UserLogin(**test_login_data)

    async def mock_get_user_by_email(user_email):
        return None

    monkeypatch.setattr(repository, "get_user_by_email", mock_get_user_by_email)

    response = test_app.post("/auth/login", data=test_login_request.json())
    assert response.status_code == 403
