from flask import Flask , request , abort, make_response
from flask.json import jsonify
from backend.models.shelter import Shelter
from backend.database import db_session
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token ,jwt_required ,get_jwt_identity
from flask import Blueprint

shelter_blueprint = Blueprint('shelter', __name__)

@shelter_blueprint.route('/',methods=['POST'])
@jwt_required
def post_shelter():
    content = request.get_json()
    if not content:
        abort(make_response(jsonify(message="no json data"), 400))
    if 'name' not in content or 'email' not in content or 'address' not in  content:
        abort(make_response(jsonify(message="all parameters must be set"), 400))
    try:
        shelter = Shelter(content['name'] , content['email'],content['address'])
        db_session.add(shelter)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        abort(make_response(jsonify(message='Shelter with this email or adress has already been registered'), 400))
    except Exception as e :
         abort(make_response(jsonify(message="bad params"), 400))
    return jsonify({'message':'success'})

@shelter_blueprint.route('/',methods = ['GET'])
def shelter_list():
    shelters=Shelter.query.all()
    return jsonify([i.serialized for i in shelters])



@shelter_blueprint.route('/<id>',methods=['GET'])
def shelter_instace(id):
    try:
        shelter=Shelter.query.get(id)
        if not shelter:
            raise Exception  
    except:       
        abort(make_response(jsonify(message='no such shelter'), 400))
    return jsonify(shelter.serialized)



@shelter_blueprint.route('/<id>',methods=['PUT','DELETE'])
@jwt_required
def shelter_modifier(id):
    try:
        shelter=Shelter.query.get(id)
        if not shelter:
            raise Exception  
    except:       
        abort(make_response(jsonify(message='no such shelter'), 400))
    if request.method == "DELETE":
        db_session.delete(shelter)
        db_session.commit()
        return(shelter.serialized)
    if request.method == "PUT":
        content = request.get_json()
        if 'name' not in content or 'email' not in content or 'address' not in  content:
            abort(400,{'message':'all required parameters must be set'})
        shelter.name = content['name']
        shelter.email = content['email']
        shelter.address = content['address']
        db_session.commit()
        return jsonify(shelter.serialized)
