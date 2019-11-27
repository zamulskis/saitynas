from flask import Flask , request , abort , make_response
from flask.json import jsonify
from backend.models.user import User
from backend.database import db_session
from sqlalchemy.exc import IntegrityError
from flask_api import status
from flask_jwt_extended import create_access_token ,jwt_required ,get_jwt_identity,create_refresh_token,jwt_required , jwt_refresh_token_required
from flask_restful import Resource, Api
from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register/',methods = ['POST'])
@jwt_required
def register():
    content = request.get_json()
    if not content:
        return "wrong format",400
    if 'username' not in content or 'email' not in content or 'password' not in  content:
        return jsonify("all parameters must be set"), 400
    try:
        user = User(content['username'] , content['email'],content['password'])
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return jsonify("Username or email is taken"), 400

    return jsonify('success') ,status.HTTP_201_CREATED

@user_blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200
    

@user_blueprint.route('/login/',methods=['POST'])
def login():
    content = request.get_json()
    if not content:
        return "wrong format",400 
    if  'email' not in content or 'password' not in  content:
        return jsonify("all parameters must be set"), 400
    user = User.query.filter_by(email=content['email'],password=content['password']).first()
    if not user :
        abort(make_response(jsonify("worng credentials"), 400))
    return jsonify({
                    'access_token': create_access_token(identity=user.serialized),
                    'refresh_token':create_refresh_token(identity=user.serialized),
    }), 200


@user_blueprint.route('/user/',methods=['GET'])
@jwt_required
def admin_get_users():
    users=User.query.all()
    return jsonify([i.serialized for i in users])

@user_blueprint.route('/user/<id>',methods=['GET','DELETE','PUT'])
@jwt_required
def admin_get_user(id):
    user=User.query.get(id)
    if not user:
        abort(make_response(jsonify(message="no such user"), 404))
    if request.method=='GET':
        return jsonify(user.serialized)
    if request.method=='DELETE':
        db_session.delete(user)
        db_session.commit()
        return jsonify(user.serialized)
    if request.method=='PUT':
        content = request.get_json()
        try:
            if 'username' in  content:
                user.username=content['username']
            if  'email' in content:
                user.email=content['email']
            if  'password' in content:
                user.password=content['password']
            db_session.add(user)
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            abort(make_response(jsonify(message="bad params"), 400))

        return jsonify(user.serialized)

