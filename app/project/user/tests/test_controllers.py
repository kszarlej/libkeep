from pytest import mark
from flask import url_for

from project.db import User
from project.utils.auth import decode_token
from project.utils.test import post

from ..controllers import db


_post_register = post(endpoint='user:register')
_post_login = post(endpoint='user:login')


def test_register_bad_data(client):
    response = _post_register(client, {
        'password': 'test_password',
    })

    assert response.status_code == 400
    assert 'email' in response.json['message']


def test_register_proper_result(client, mocker):
    mocker.patch.object(db, 'session')

    response = _post_register(client, {
        'email': 'test@example.com',
        'password': 'test_password',
    })

    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


@mark.integration
def test_register_db_insert(client, db):
    data = {
        'email': 'test@example.com',
        'password': 'test_password',
    }

    response = _post_register(client, data)

    assert response.status_code == 200
    assert User.query.filter_by(email=data['email']).first()


def test_login_bad_data(client):
    response = _post_login(client, {
        'password': 'test_password',
    })

    assert response.status_code == 400
    assert 'email' in response.json['message']


@mark.integration
def test_login_user_not_found(client, db):
    response = _post_login(client, {
        'email': 'not_exists@example.com',
        'password': 'test_password',
    })

    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert 'default' in response.json['message']


@mark.integration
def test_login_user_bad_password(client, user):
    response = _post_login(client, {
        'email': user.email,
        'password': 'bad_password',
    })

    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert 'default' in response.json['message']


@mark.integration
def test_login_user_proper_data(client, user):
    response = _post_login(client, {
        'email': user.email,
        'password': 'test_password',
    })

    assert response.status_code == 200
    assert 'token' in response.json


@mark.integration
def test_login_user_valid_token(client, user):
    response = _post_login(client, {
        'email': user.email,
        'password': 'test_password',
    })

    token_data = decode_token(response.json['token'])

    assert token_data['email'] == user.email
    assert token_data['id'] == user.id
    assert not token_data['is_admin']
