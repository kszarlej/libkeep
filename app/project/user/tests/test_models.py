from pytest import fixture, mark

from project.db import User


@fixture
def user():
    user = User()
    user.password = 'plain_text_password'

    return user


def test_user_to_str_email_none(user):
    assert str(user) == str(None)


def test_user_to_str(user):
    user.email = 'test@example.com'

    assert str(user) == user.email


@mark.slowtest
def test_secure_password(user):
    test_password = user.password

    user.secure_password()

    assert user.password != test_password


@mark.slowtest
def test_verify_password(user):
    test_password = user.password
    user.secure_password()

    assert user.verify_password(test_password)


@mark.slowtest
def test_verify_bad_password(user):
    test_password = user.password
    user.secure_password()

    assert not user.verify_password(test_password + 'a')
