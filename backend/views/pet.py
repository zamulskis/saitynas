from flask import Flask , request , abort , make_response
from flask.json import jsonify
from backend.models.pet import Pet,Species
from backend.database import db_session
from sqlalchemy.exc import IntegrityError
from flask_api import status
from flask_jwt_extended import create_access_token ,jwt_required ,get_jwt_identity
from flask import Blueprint
from backend.models.shelter import Shelter


pet_blueprint = Blueprint('pet', __name__)
species_blueprint = Blueprint('species', __name__)

@species_blueprint.route('/',methods = ['POST'])
@jwt_required
def species_post():
    if request.method == 'POST':
        try:
            content = request.get_json()
            if not content:
                return jsonify({"msg":"wrong format"}),400
            if 'name' not in content:
                abort(make_response(jsonify(message="all parameters must be set"), 400))
            new_species = Species(content['name'])
            db_session.add(new_species)
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            abort(make_response(jsonify(message="species already exists"), 400))
        except Exception as e :
            abort(500,{'message':str(e)})
        return jsonify({'message':'success'}),status.HTTP_201_CREATED
    return abort(404)

@species_blueprint.route('/',methods = ['GET'])
def species_get():
    if request.method == 'GET':
        all_species=Species.query.all()
        return jsonify([i.serialized for i in all_species])

@species_blueprint.route('/<id>',methods = ['GET'])
def species_instace(id):
    if not Species.query.get(id):
        abort(make_response(jsonify(message="no such species"), 400))
    if request.method == 'GET':
        species_instace=Species.query.get(id)
        return jsonify(species_instace.serialized)

@species_blueprint.route('/<id>',methods = (['DELETE','PUT']))
@jwt_required
def delete_sepcies(id):
    if not Species.query.get(id):
        abort(make_response(jsonify(message="no such species"), 400))
    if request.method=='DELETE':
        species_instace=Species.query.get(id)
        db_session.delete(species_instace)
        db_session.commit()
        return jsonify('Deleted'),200
    if request.method =='PUT':
        species_instace=Species.query.get(id)
        content = request.get_json()
        if not content:
            return "wrong format",400
        if 'name' not in content:
            abort(make_response(jsonify(message="all parameters must be set"), 400))
        try:
            species_instace.name = content['name']
            db_session.commit()
        except:
             abort(make_response(jsonify(message="name is taken"), 400))
        return jsonify(species_instace.serialized)




@pet_blueprint.route('/',methods = ['GET'])
def shelters_pets(shelter):
    if not shelter:
        abort(make_response(jsonify(message="no such shelter"), 404))
    if request.method == 'GET':
        all_pets=Pet.query.filter_by(shelter=shelter)
        return jsonify([i.serialized for i in all_pets])

@pet_blueprint.route('/<id>',methods = ['GET'])
def shelters_pet(shelter , id):
    if not shelter:
        abort(make_response(jsonify(message="no such shelter"), 404))
    pet = Pet.query.get(id)
    if not pet.shelter == shelter:
        abort(make_response(jsonify(message="no such pet"), 404))
    if request.method == 'GET':
        return jsonify(pet.serialized)

@pet_blueprint.route('/<id>',methods = (['DELETE','PUT']))
@jwt_required
def shelters_pet_admin(shelter ,id):
    if not shelter:
        return "not found " ,404
    pet = Pet.query.get(id)
    if not pet.shelter is shelter:
        abort(make_response(jsonify(message="no such pet"), 400))
    if request.method=='DELETE':
        pet_Instance=Pet.query.get(id)
        db_session.delete(pet_Instance)
        db_session.commit()
        return jsonify(200,'Deleted')
    if request.method =='PUT':
        pet_Instance=Pet.query.get(id)
        content = request.get_json()
        if not content:
            return "wrong format",400
        try:
            if "name" in content :
                pet_Instance.name=content["name"]
            if "age" in content:
                pet_Instance.age=content["age"]
            if "shelter" in content:
                shelter_next = Shelter.query.get(content['shelter'])
                if not shelter_next:
                    return "not found " ,404
                pet_Instance.shelter=content['shelter']
        except:
           abort(make_response(jsonify(message="validation failed"), 400))
        db_session.commit()
        return jsonify(pet_Instance.serialized)

@pet_blueprint.route('/',methods = ['POST'])
@jwt_required
def shelters_pets_admin(shelter):
    if not shelter:
        return "not found " ,404
    if request.method=='POST':
        content = request.get_json()
        if not content:
            return "wrong format",400
        if "name" not in content or "age"  not in content   or "species" not in content or "description" not in content:
              abort(make_response(jsonify(message="all params must be set"), 400))
        try:
            pet_Instance=  Pet(content['name'],content['age'],content['species'],content['description'],shelter)
            db_session.add(pet_Instance)
            db_session.commit()
            return jsonify('created'),200
        except Exception as exception:
            return jsonify(str(exception)),400
            
    
    #    name = Column(String(50))
    # age = Column(String(50))
    # description = Column(String(255))
    # species = Column(Integer, ForeignKey('species.id'))
    # shelter = Column(Integer, ForeignKey('shelters.id'))

# @app.route('/pet/<shelter>/pets/<species>/',methods = ['GET'])
# def shelters_species(shelter,species):
#     if request.method == 'GET':
#         all_pets=Pet.query.filter_by(shelter=shelter,species=species)
#         return jsonify([{i.id:i.serialized} for i in all_pets])
#     return abort(404)

# # @app.route('/shelter/pets/<id>/',methods=['GET','PATCH','DELETE'])
# # def shleter_instace(id):
# #     try:
# #         shelter=Shelter.query.get(id)
# #         if not shelter:
# #             raise Exception  
# #     except:       
# #         abort(400,{'message':'no such shelter'})
# #     if request.method == "GET":
# #         return jsonify(shelter.serialized)
# #     if request.method == "DELETE":
# #         db_session.delete(shelter)
# #         db_session.commit()
# #         return(shelter.serialized)
# #     if request.method == "PATCH":
# #         content = request.get_json()
# #         if 'name' not in content or 'email' not in content or 'address' not in  content:
# #             abort(400,{'message':'all required parameters must be set'})
# #         shelter.name = content['name']
# #         shelter.email = content['email']
# #         shelter.address = content['address']
# #         db_session.commit()
# #         return jsonify(shelter.serialized)

# #     return abort(404)
