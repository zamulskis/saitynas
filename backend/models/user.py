from sqlalchemy import Column, Integer, String
from flask import abort , jsonify
from sqlalchemy.orm import validates
from backend.database import Base

ROLES = ['Admin','User']
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    role = Column(Integer())

    def __init__(self, name=None, email=None , password=None , role=1):
        self.name = name
        self.email = email
        self.password = password
        self.role=role

    def __repr__(self):
        return '<User %r>' % (self.name)
    @property
    def serialized(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'role':ROLES[int(self.role)],
        }
    
    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email,password=password).first()
        return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return User.query.filter_by.get(user_id, None)
        
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email ,abort(400,{'message':'invalid email'})
        return email
