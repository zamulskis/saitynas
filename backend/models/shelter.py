from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask import abort , jsonify
from sqlalchemy.orm import validates
from backend.database import Base

class Shelter(Base):
    __tablename__ = 'shelters'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    address = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    pets = relationship('Pet')

    def __init__(self, name=None, email=None , address=None ):
        self.name = name
        self.email = email
        self.address = address

    def __repr__(self):
        return '<Shelter %r>' % (self.name) + ' '+self.address
    @property
    def serialized(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'address':self.address,
        }
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email ,abort(400,{'message':'invalid email'})
        return email
    