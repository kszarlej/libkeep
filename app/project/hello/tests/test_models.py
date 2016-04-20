from ..models import User


def test_user(db):
    assert User.query.count() == 0

    u1 = User('name', 'email')
    db.session.add(u1)
    db.session.commit()

    assert User.query.count() == 1


def test_db_fixute(db):
    assert User.query.count() == 0
