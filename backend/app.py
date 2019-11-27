from flask import Flask
from flask_jwt_extended import JWTManager
from .views import shelter_blueprint ,pet_blueprint ,user_blueprint , species_blueprint
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
app.register_blueprint(shelter_blueprint,url_prefix="/shelter")
app.register_blueprint(species_blueprint,url_prefix="/species")
app.register_blueprint(pet_blueprint ,url_prefix="/shelter/<int:shelter>/pet/")
app.register_blueprint(user_blueprint)
if __name__ == "__main__":
    app.run(debug=True,port=8080)

