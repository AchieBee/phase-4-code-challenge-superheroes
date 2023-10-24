#!/usr/bin/env python3
from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

# Import models
from models import Hero, Power, Hero_Power

# Define root route
@app.route('/')
def home():
    return '<h1>Welcome Home</h1>'

# Define a base resource for common response methods
class BaseResource(Resource):
    def make_response(self, data, status_code):
        response = make_response(jsonify(data), status_code)
        return response

# GET (/heroes)
class Heroes(BaseResource):
    def get(self):
        heroes = Hero.query.all()
        heroes_data = [
            {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "created_at": hero.created_at
            }
            for hero in heroes
        ]
        return self.make_response(heroes_data, 200)
api.add_resource(Heroes, '/heroes')

# GET (/heroes/:id)
class HeroesById(BaseResource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {
                        "id": power.id,
                        "name": power.name,
                        "description": power.description
                    }
                    for power in hero.powers
                ]
            }
            return self.make_response(hero_data, 200)
        else:
            return self.make_response({"error": "Hero not found"}, 404)
api.add_resource(HeroesById, '/heroes/<int:id>')

# GET (/powers)
class Powers(BaseResource):
    def get(self):
        powers = Power.query.all()
        powers_data = [
            {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at,
                "hero_ps": [
                    {
                        "strength": hero_p.strength,
                        "hero_id": hero_p.hero_id
                    }
                    for hero_p in power.hero_ps
                ]
            }
            for power in powers
        ]
        return self.make_response(powers_data, 200)
api.add_resource(Powers, '/powers')

# GET (/powers/:id)
class PowersById(BaseResource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at,
                "hero_ps": [
                    {
                        "strength": hero_p.strength,
                        "hero_id": hero_p.hero_id
                    }
                    for hero_p in power.hero_ps
                ]
            }
            return self.make_response(power_data, 200)
        else:
            return self.make_response({"error": "Power not found"}, 404)
api.add_resource(PowersById, '/powers/<int:id>')

# PATCH (/powers/:id)
class UpdatePower(BaseResource):
    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return self.make_response({"error": "Power not found"}, 404)

        description = request.form.get('description')

        if not description or len(description) < 20:
            return self.make_response({"errors": ["validation errors"]}, 400)

        for attr in request.form:
            setattr(power, attr, request.form.get(attr))
        db.session.add(power)
        db.session.commit()

        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
            "created_at": power.created_at
        }

        return self.make_response(power_data, 200)
api.add_resource(UpdatePower, '/powers/<int:id>')

# POST (/hero_powers)
class HeroPowers(BaseResource):
    def post(self):
        valid_strengths = ["Strong", "Weak", "Average"]
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        if strength not in valid_strengths:
            return self.make_response({"errors": ["validation errors"]}, 400)

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return self.make_response({"error": "Invalid hero_id or power_id"}, 404)

        hero_power_entry = Hero_Power(
            hero_id=hero_id,
            power_id=power_id,
            strength=strength
        )

        db.session.add(hero_power_entry)
        db.session.commit()

        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description
                }
                for p in hero.powers
            ]
        }
        return self.make_response(hero_data, 201)
api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)
