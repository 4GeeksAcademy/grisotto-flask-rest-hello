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
from models import db, User
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
