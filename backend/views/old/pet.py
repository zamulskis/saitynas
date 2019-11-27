# from flask import Flask , request , abort , make_response
# from flask.json import jsonify
# from backend.app import app
# from backend.models.pet import Pet,Species
# from backend.database import db_session
# from sqlalchemy.exc import IntegrityError
# from flask_api import status
# from flask_jwt_extended import create_access_token ,jwt_required ,get_jwt_identity

# @app.route('/species/',methods = ['GET','POST'])
# def species():
#     if request.method == 'POST':
#         try:
#             content = request.get_json()
#             if 'name' not in content:
#                 abort(make_response(jsonify(message="all parameters must be set"), 400))
#             new_species = Species(content['name'])
#             db_session.add(new_species)
#             db_session.commit()
#         except IntegrityError:
#             db_session.rollback()
#             abort(make_response(jsonify(message="species already exists"), 400))
#         except Exception as e :
#             abort(500,{'message':str(e)})
#         return jsonify({'message':'success'}),status.HTTP_201_CREATED
#     if request.method == 'GET':
#         all_species=Species.query.all()
#         return jsonify([{i.id:i.serialized} for i in all_species])
#     return abort(404)

# @app.route('/species/<id>/',methods = ['GET'])
# def species_instace(id):
#     if not Species.query.get(id):
#         abort(make_response(jsonify(message="no such species"), 400))
#     if request.method == 'GET':
#         species_instace=Species.query.get(id)
#         return jsonify(species_instace.serialized)

# @app.route('/species/<id>/',methods = (['DELETE','PUT']))
# def delete_sepcies(id):
#     if not Species.query.get(id):
#         abort(make_response(jsonify(message="no such species"), 400))
#     if request.method=='DELETE':
#         species_instace=Species.query.get(id)
#         db_session.delete(species_instace)
#         db_session.commit()
#         return jsonify(200,'Deleted')
#     if request.method =='PUT':
#         species_instace=Species.query.get(id)
#         content = request.get_json()
#         if 'name' not in content:
#             abort(make_response(jsonify(message="all parameters must be set"), 400))
#         try:
#             species_instace.name = content['name']
#         except:
#             abort('this name is not valid')
#         db_session.commit()
#         return jsonify(species_instace.serialized)



# @app.route('/pet/',methods = ['GET','POST'])
# def pet():
#     if request.method == 'POST':
#         content = request.get_json()
#         if 'name' not in content or 'age' not in content or 'species' not in  content or 'description' not in  content or 'shelter' not in  content:
#             abort(make_response(jsonify(message="all parameters must be set"), 400))
#         try:
#             new_pet = Pet(content['name'],content['age'],content['species'],content['description'],content['shelter'])
#             db_session.add(new_pet)
#             db_session.commit()
#         except IntegrityError:
#             db_session.rollback()
#             abort(make_response(jsonify(message="pet already exsits"), 400))
#         except Exception as e :
#             abort(make_response(jsonify(message=str(e)), 400))
#         return jsonify({'message':'success'}),status.HTTP_201_CREATED
#     if request.method == 'GET':
#         all_pets=Pet.query.all()
#         return jsonify([{i.id:i.serialized} for i in all_pets])
#     return abort(404)

# @app.route('/pet/<id>/',methods = ['GET'])
# def pet_instace(id):
#     if request.method == 'GET':
#         try:
#             pets=Pet.query.get(id)
#         except:
#             abort(make_response(jsonify(message="no such pet"), 404))
#         return jsonify(pets.serialized)
#     return abort(404)

# # @app.route('/shelter/<shelter>/pets/',methods = ['GET'])
# # def shelters_pets(shelter):
# #     if request.method == 'GET':
# #         all_pets=Pet.query.filter_by(shelter=shelter)
# #         return jsonify([{i.id:i.serialized} for i in all_pets])
# #     return abort(404)

# # @app.route('/pet/<shelter>/pets/<species>/',methods = ['GET'])
# # def shelters_species(shelter,species):
# #     if request.method == 'GET':
# #         all_pets=Pet.query.filter_by(shelter=shelter,species=species)
# #         return jsonify([{i.id:i.serialized} for i in all_pets])
# #     return abort(404)

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
