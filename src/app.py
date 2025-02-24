"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Vehicles, Favorite_planets, Favorite_people, Favorite_vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [User.serialize(user) for user in users]

    return jsonify(result), 200



@app.route('/users/<int:id>/', methods=['GET'])
def get_unique_user(id):
    user = User.query.get(id)
    if user:
        result = user.serialize()
    else: 
        result = {"msg": "That user doesn't exist, please make sure you are writing the rigth user id"}
    return jsonify(result), 200



@app.route('/planets', methods=['GET'])
def get_planet():
    planets = Planets.query.all()
    result = [Planets.serialize(planet) for planet in planets]
    
    return jsonify(result), 200


@app.route('/planets/<int:id>/', methods=['GET'])
def get_unique_planet(id):
    planet = Planets.query.get(id)
    result = planet.serialize()
    return jsonify(result), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    result = [People.serialize(person) for person in people]
    
    return jsonify(result), 200


@app.route('/people/<int:id>/', methods=['GET'])
def get_unique_person(id):
    person = People.query.get(id)
    result = person.serialize()
    return jsonify(result), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    result = [Vehicles.serialize(vehicle) for vehicle in vehicles]
    
    return jsonify(result), 200


@app.route('/vehicles/<int:id>/', methods=['GET'])
def get_unique_vehicle(id):
    vehicle = Vehicles.query.get(id)
    result = vehicle.serialize()
    return jsonify(result), 200

@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    user_serialized = user.serialize()
    favorite_people = user_serialized['favorite_people']
    favorite_planets = user_serialized['favorite_planets']
    favorite_vehicles = user_serialized['favorite_vehicles']
    return jsonify(favorite_people, favorite_planets, favorite_vehicles), 200



@app.route('/users/<int:id>/favorites/planet/<int:id_planet>', methods=['POST'])
def post_planet_favorite(id, id_planet):
    exist = Favorite_planets.query.filter_by(user_id = id, planet_id = id_planet).first()
    if exist:
        return jsonify({"msg": "This favorite already exist"}),400
    
    new_favorite_planet = Favorite_planets(user_id= id, planet_id= id_planet)
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify({"msg" : "Favorite added"}), 200



@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def post_people_favorite(user_id,people_id):
    exist = Favorite_people.query.filter_by(user_id =user_id, people_id = people_id).first()
    if exist:
        return jsonify({"msg": "This favorite already exist"}),400
    
    new_favorite_people = Favorite_planets(user_id= id, people_id = people_id)
    db.session.add(new_favorite_people)
    db.session.commit()
    return jsonify({"msg" : "Favorite added"}), 200



@app.route('/users/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['POST'])
def post_vechicle_favorite(user_id, vehicle_id):
    exist = Favorite_vehicles.query.filter_by(user_id = user_id, vehicle_id = vehicle_id).first()
    if exist:
        return jsonify({"msg": "This favorite already exist"}),400
    
    new_favorite_vehicle = Favorite_vehicles(user_id= user_id, vehicle_id = vehicle_id )
    db.session.add(new_favorite_vehicle)
    db.session.commit()
    return jsonify({"msg" : "Favorite added"}), 200

@app.route('/users/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    exist = Favorite_vehicles.query.filter_by(user_id= user_id, vehicle_id = vehicle_id).first()
    if exist:
        db.session.delete(exist)
        db.session.commit()
        return jsonify({"msg": "Favorite removed"})
    return jsonify({"msg": "This favorite doesn't exist, try another one"})

@app.route('/users/<int:user_id>/favorites/vehicle/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    exist = Favorite_planets.query.filter_by(user_id= user_id, planet_id = planet_id).first()
    if exist:
        db.session.delete(exist)
        db.session.commit()
        return jsonify({"msg": "Favorite removed"})
    return jsonify({"msg": "This favorite doesn't exist, try another one"})

@app.route('/users/<int:user_id>/favorites/vehicle/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    exist = Favorite_people.query.filter_by(user_id= user_id, people_id = people_id).first()
    if exist:
        db.session.delete(exist)
        db.session.commit()
        return jsonify({"msg": "Favorite removed"})
    return jsonify({"msg": "This favorite doesn't exist, try another one"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
