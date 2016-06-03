from project.db import db, User


def create_admin(admin_email, admin_password):

    if not User.query.filter_by(email=admin_email).count():
        user = User()
        user.email = admin_email
        user.password = admin_password
        user.secure_password()
        user.is_admin = True

        db.session.add(user)
        db.session.commit()
