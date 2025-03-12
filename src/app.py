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
    existing_character = Character.query.filter_by(name=request_body["name"]).first()
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

@app.route('/user', methods=['GET'])
def handle_user():
    user = User.query.all()

    return jsonify(user.serialize()), 200

    # response_body = {
    #     "id": "self.id",
    #     "email": "self.email",
    # }

    # return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def handle_people():

    response_body = {
        "results": [
            {
                "uid": "1",
                "name": "Luke Skywalker",
                "url": "https://www.swapi.tech/api/people/1"
            },
            {
                "uid": "2",
                "name": "C-3PO",
                "url": "https://www.swapi.tech/api/people/2"
            },
            {
                "uid": "3",
                "name": "R2-D2",
                "url": "https://www.swapi.tech/api/people/3"
            },
            {
                "uid": "4",
                "name": "Darth Vader",
                "url": "https://www.swapi.tech/api/people/4"
            },
            {
                "uid": "5",
                "name": "Leia Organa",
                "url": "https://www.swapi.tech/api/people/5"
            },
            {
                "uid": "6",
                "name": "Owen Lars",
                "url": "https://www.swapi.tech/api/people/6"
            },
            {
                "uid": "7",
                "name": "Beru Whitesun lars",
                "url": "https://www.swapi.tech/api/people/7"
            },
            {
                "uid": "8",
                "name": "R5-D4",
                "url": "https://www.swapi.tech/api/people/8"
            },
            {
                "uid": "9",
                "name": "Biggs Darklighter",
                "url": "https://www.swapi.tech/api/people/9"
            },
            {
                "uid": "10",
                "name": "Obi-Wan Kenobi",
                "url": "https://www.swapi.tech/api/people/10"
            }
        ]


    }

    return jsonify(response_body), 200


@app.route('/people<int:people_id>', methods=['GET'])
def handle_people_id():

    response_body = {
        "result": {
            "properties": {
                "name": "Luke Skywalker",
                "gender": "male",
                "skin_color": "fair",
                "hair_color": "blond",
                "height": "172",
                "eye_color": "blue",
                "mass": "77",
                "homeworld": "https://www.swapi.tech/api/planets/1",
                "birth_year": "19BBY",
                "url": "https://www.swapi.tech/api/people/1"
            }

        }

    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def planets():

    response_body = {
        "results": [
        {
            "uid": "1",
            "name": "Tatooine",
            "url": "https://www.swapi.tech/api/planets/1"
        },
        {
            "uid": "2",
            "name": "Alderaan",
            "url": "https://www.swapi.tech/api/planets/2"
        },
        {
            "uid": "3",
            "name": "Yavin IV",
            "url": "https://www.swapi.tech/api/planets/3"
        },
        {
            "uid": "4",
            "name": "Hoth",
            "url": "https://www.swapi.tech/api/planets/4"
        },
        {
            "uid": "5",
            "name": "Dagobah",
            "url": "https://www.swapi.tech/api/planets/5"
        },
        {
            "uid": "6",
            "name": "Bespin",
            "url": "https://www.swapi.tech/api/planets/6"
        },
        {
            "uid": "7",
            "name": "Endor",
            "url": "https://www.swapi.tech/api/planets/7"
        },
        {
            "uid": "8",
            "name": "Naboo",
            "url": "https://www.swapi.tech/api/planets/8"
        },
        {
            "uid": "9",
            "name": "Coruscant",
            "url": "https://www.swapi.tech/api/planets/9"
        },
        {
            "uid": "10",
            "name": "Kamino",
            "url": "https://www.swapi.tech/api/planets/10"
        }
    ]

    }

    return jsonify(response_body), 200


@app.route('/planets<int:planets_id>', methods=['GET'])
def handle_planets_id():

    response_body = {
        "result": {
            "properties": {
                "created": "2025-02-28T18:09:54.727Z",
                "edited": "2025-02-28T18:09:54.727Z",
                "climate": "frozen",
                "surface_water": "100",
                "name": "Hoth",
                "diameter": "7200",
                "rotation_period": "23",
                "terrain": "tundra, ice caves, mountain ranges",
                "gravity": "1.1 standard",
                "orbital_period": "549",
                "population": "unknown",
                "url": "https://www.swapi.tech/api/planets/4"
            } 
        }  

    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
