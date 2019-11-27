from flask import Flask , request , abort, make_response
from flask.json import jsonify
from backend.app import app
from backend.models.shelter import Shelter
from backend.database import db_session
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token ,jwt_required ,get_jwt_identity

@app.route('/shelter/',methods = ['GET','POST'])
def shelter():
    if request.method == 'POST':
        content = request.get_json()
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
            abort(500,{'message':str(e)})
        return jsonify({'message':'success'})
    if request.method == 'GET':
        shelters=Shelter.query.all()
        return jsonify([{i.id:i.serialized} for i in shelters])
    return abort(404)

@app.route('/shelter/<id>/',methods=['GET','PUT','DELETE'])
def shleter_instace(id):
    try:
        shelter=Shelter.query.get(id)
        if not shelter:
            raise Exception  
    except:       
        abort(make_response(jsonify(message='no such shelter'), 400))
    if request.method == "GET":
        return jsonify(shelter.serialized)
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

    return abort(404)
