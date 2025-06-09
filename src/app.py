"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

# archivo app.py me va a servir para hacer los endpoints

import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Fav_character, Fav_planets, Planets

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

# endpoints


@app.route('/users', methods=['GET'])
def get_users():
    try:
        query_results = User.query.all()

        if not query_results:
            return jsonify({"msg": "No users Found"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "ok",
            "results": results
        }

        return jsonify(response_body), 200


    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        query_results = Character.query.all()
        if not query_results:
            return jsonify({"msg": "No characters found"}), 400
        results = list(map(lambda character: character.serialize(), query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"msg": "Character not found"}), 404
        return jsonify(character.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500
    

@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        query_results = Planets.query.all()
        if not query_results:
            return jsonify({"msg": "No planets found"}), 400
        results = list(map(lambda planet: planet.serialize(), query_results))
        response_body = {
            "msg": "ok",
            "results": results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planets.query.get(planet_id) 
        if not planet:
            return jsonify({"msg": "Planet not found"}), 404
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

#create user 

@app.route('/character/<int:character_id>', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"msg": "no se proporcionaron datos"}), 400

    email = data.get('email')
    password = data.get('password')
    is_active = data.get('is_active', False)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "ya existe un usuario con ese mail"}), 409

    new_user = User(
        email=email,
        password=password,
        is_active=is_active
    )
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

# Favorites for current user
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"msg": "user_id is required"}), 400
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "user not found"}), 404
        return jsonify(user.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"msg": "user_id is required"}), 400
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "user not found"}), 404 
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({"msg": "planet not found"}), 404
        
        
        for planet in user.favorite_planets:
            if planet.id ==planet_id: 
                return jsonify({"msg": "planet already exist in favorites"}), 400

        favorite = Fav_planets(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"msg": "Planet added to favorites"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"msg": "user_id is required"}), 400
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "user not found"}), 404
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"msg": "character not found"}), 404
        
        for character in user.favorite_characters:
            if character.id ==character_id: 
                return jsonify({"msg": "character already exist in favorites"}), 400

        favorite = Fav_character(user_id=user_id, character_id=character_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"msg": "Character added to favorites"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"msg": "user_id is required"}), 400

        favorite = Fav_planets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if not favorite:
            return jsonify({"msg": "Favorite not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": "Planet from favorites deleted"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

@app.route('/favorite/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"msg": "user_id is required"}), 400

        favorite = Fav_character.query.filter_by(user_id=user_id, character_id=character_id).first()
        if not favorite:
            return jsonify({"msg": "Favorite not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": "Character from favorites deleted"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

# Main
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
