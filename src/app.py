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
from models import db, User, Character, Favorite, Planet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

# To create new users, characters, and planets in the table for testing (SQLAlchemy 2.0 DOES NOT SUPPORT flask_admin)
# To create new users, characters, and planets in the table for testing (SQLAlchemy 2.0 DOES NOT SUPPORT flask_admin)
# To create new users, characters, and planets in the table for testing (SQLAlchemy 2.0 DOES NOT SUPPORT flask_admin)


@app.route('/user', methods=['POST'])
def create_user():
    """
    Create a new user
    """
    request_body = request.get_json()

    # Check if required fields are provided
    if not request_body.get("email") or not request_body.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    # Check if user with same email already exists
    existing_user = User.query.filter_by(email=request_body["email"]).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 400

    # Create new user
    new_user = User(
        email=request_body["email"],
        password=request_body["password"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201


@app.route('/character', methods=['POST'])
def create_character():
    """
    Create a new character
    """
    request_body = request.get_json()

    # Check if required fields are provided
    if not request_body.get("name"):
        return jsonify({"message": "Character name is required"}), 400

    # Check if character with same name already exists
    existing_character = Character.query.filter_by(
        name=request_body["name"]).first()
    if existing_character:
        return jsonify({"message": "Character with this name already exists"}), 400

    # Create new character
    new_character = Character(
        name=request_body["name"],
        gender=request_body.get("gender"),
        skin_color=request_body.get("skin_color"),
        hair_color=request_body.get("hair_color"),
        height=request_body.get("height"),
        eye_color=request_body.get("eye_color"),
        mass=request_body.get("mass"),
        homeworld=request_body.get("homeworld"),
        birth_year=request_body.get("birth_year")
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 201


@app.route('/planet', methods=['POST'])
def create_planet():
    """
    Create a new planet
    """
    request_body = request.get_json()

    # Check if required fields are provided
    if not request_body.get("name"):
        return jsonify({"message": "Planet name is required"}), 400

    # Check if planet with same name already exists
    existing_planet = Planet.query.filter_by(name=request_body["name"]).first()
    if existing_planet:
        return jsonify({"message": "Planet with this name already exists"}), 400

    # Create new planet
    new_planet = Planet(
        name=request_body["name"],
        climate=request_body.get("climate"),
        surface_water=request_body.get("surface_water"),
        diameter=request_body.get("diameter"),
        rotation_period=request_body.get("rotation_period"),
        gravity=request_body.get("gravity"),
        orbital_period=request_body.get("orbital_period"),
        population=request_body.get("population")
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

# End of POST routes to add new user, character, and planet for testing purposes
# End of POST routes to add new user, character, and planet for testing purposes
# End of POST routes to add new user, character, and planet for testing purposes


@app.route('/users', methods=['GET'])
def handle_user():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200


@app.route('/users/favorites', methods=['GET'])
def handle_favorites():
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User Does not exist", status_code=404)

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in favorites]

    return jsonify(serialized_favorites), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def favorite_planet(planet_id):
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User Does not exist", status_code=404)

    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet Does not exist", status_code=404)

    favorite = Favorite(name=planet.name, user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "favorite planet added succesfully"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def favorite_people(people_id):
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User Does not exist", status_code=404)

    character = Character.query.get(people_id)
    if character is None:
        raise APIException("character Does not exist", status_code=404)

    favorite = Favorite(name=character.name,
                        user_id=user_id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "favorite character added succesfully"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def favorite_delete(people_id):
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        # raise APIException("User Does not exist", status_code=404)
        return jsonify({"message": "User does not exist"}), 404

    favorite = Favorite.query.filter_by(
        user_id=user_id, character_id=people_id).first()
    if favorite is None:
        # raise APIException("favorite character Does not exist", status_code=404)
        return jsonify({"message": "Favorite character does not exist"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "favorite character deleted succesfully"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def favorite_planet_delete(planet_id):
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User does not exist"}), 404
        # raise APIException("User Does not exist", status_code=404)

    favorite = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        # raise APIException(
            # "favorite character Does not exist", status_code=404)
        return jsonify({"message": "Favorite planet does not exist"}), 404    

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "favorite planet deleted succesfully"}), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people_id(people_id):
    person = Character.query.get(people_id)
    if person is None:
        raise APIException("Character Does not exist", status_code=404)

    return jsonify(person.serialize()), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet Does not exist", status_code=404)

    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['GET'])
def planets():
    all_planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in all_planets]

    return jsonify(serialized_planets), 200


@app.route('/people', methods=['GET'])
def people():
    people = Character.query.all()
    serialized_people = [person.serialize() for person in people]

    return jsonify(serialized_people), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
