from flask_security import RoleMixin
from app import db

class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    @classmethod
    def get_all_roles(cls):
        roles = cls.query.all()
        return [{'id': role.id, 'name': role.name} for role in roles]