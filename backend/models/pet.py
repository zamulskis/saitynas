from sqlalchemy import Column, Integer, String , ForeignKey
from flask import abort , jsonify
from backend.models.shelter import Shelter
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from backend.database import Base

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True)
    name = Column(String(50),unique=True)
    pets = relationship('Pet')

    def __init__(self, name=None):
        self.name = name.lower().capitalize()
    
    @property
    def serialized(self):
        return {
            'id':self.id,
            'name':self.name,
                 # 'pets':[i.serialized for i in self.pets]
        }

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(String(50))
    description = Column(String(255))
    species = Column(Integer, ForeignKey('species.id'))
    shelter = Column(Integer, ForeignKey('shelters.id'))


    def __init__(self, name=None, age=None , species=None ,description=None , shelter=None ):
        self.name = name
        self.age = age
        if not Species.query.get(species):
            abort(400,'theres no such species')
        self.species = species
        self.description=description
        if not Shelter.query.get(shelter):
            abort(400,'theres no such shelter')
        self.shelter=shelter

    def __repr__(self):
        return '<Pet %r>' % (self.name) + ' '+self.species

    @property
    def serialized(self):
        return {
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'species': self.species,
            'description': self.description,
            'shelter':self.shelter
        }