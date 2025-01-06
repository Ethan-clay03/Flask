from flask_security import SQLAlchemyUserDatastore
from app import db

class RoleUsers:
    roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key=True, index=True),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
    )

    @staticmethod
    def get_datastore():
        from app.models.role import Role
        from app.models.user import User
        return SQLAlchemyUserDatastore(db, User, Role)

    @staticmethod
    def add_role_to_user(user, role_name):
        from app.models.role import Role
        role = Role.query.filter_by(name=role_name).first()
        if role and role not in user.roles:
            user.roles.append(role)
            db.session.commit()
