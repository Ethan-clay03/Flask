from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db
import os

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    @classmethod
    def create_user(cls, username, email, password, role_name='user'):
        from app.models import Role
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = cls(username=username, email=email, password=hashed_password, fs_uniquifier=os.urandom(32).hex())
    
        role = Role.query.filter_by(name=role_name).first()
        if role:
            new_user.role = role
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @classmethod
    def search_user_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def search_user_by_email(cls, user_email):
        return cls.query.filter_by(email=user_email).first()
    
    @classmethod
    def search_user_by_username(cls, user_name):
        return cls.query.filter_by(username=user_name).first()
    
    @classmethod
    def change_user_password(cls, email, password):
        user = cls.search_user_by_email(email)
        if user is None:
            raise ValueError("Error")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user.password = hashed_password
        db.session.commit()

    @classmethod
    def get_user_role(cls, user_id):
        user = cls.query.get(user_id)
        if user and user.role:
            return user.role.name
        return None
    
    @classmethod
    def get_all_users(cls):
        return cls.query.all()
    
    @classmethod
    def delete_user(cls, user_id = None):

        user =  cls.search_user_id(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        
        return False
