from sqlalchemy import Column, Integer, String , ForeignKey ,DateTime
from flask import abort , jsonify
from backend.models.pet import Pet
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from backend.database import Base


class Assigment(Base):
    __tablename__ = 'assigment'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    time = Column(DateTime())
    pet = Column(Integer, ForeignKey('pets.id'))


    def __init__(self, name=None, email=None , time=None ,pet=None ):
        self.name = name
        self.email = email
        if not Pet.query.get(pet):
            abort(400,'theres no such pet')
        self.time = time
        self.pet = pet


    def __repr__(self):
        return '<Pet %r>' % (self.name) + ' '+self.pet

    @property
    def serialized(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'time': self.time,
            'pet': self.description,
        }

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email ,abort(400,'invalid email')
        return email
