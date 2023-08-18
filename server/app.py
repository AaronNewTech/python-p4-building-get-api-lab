#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import func
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []

    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at,
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    bakery_dict = bakery.to_dict()

    response = make_response(jsonify(bakery_dict),        
    200
    )

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    response_data = []

    for baked_good in baked_goods_by_price:
        bakery = baked_good.bakery

        if bakery is None:
            continue  # Skip this baked good if no associated bakery

        baked_good_dict = {
            "bakery": {
                "created_at": bakery.created_at,
                "id": bakery.id,
                "name": bakery.name,
                "updated_at": bakery.updated_at,
            },
            "bakery_id": bakery.id,
            "created_at": baked_good.created_at,
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "updated_at": baked_good.updated_at,
        }
        response_data.append(baked_good_dict)

    return jsonify(response_data), 200


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive:
        bakery = most_expensive.bakery

        response_data = {
            "bakery": {
                "created_at": bakery.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "id": bakery.id,
                "name": bakery.name,
                "updated_at": bakery.updated_at.strftime("%Y-%m-%d %H:%M:%S") if bakery.updated_at else None,
            },
            "bakery_id": bakery.id,
            "created_at": most_expensive.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "id": most_expensive.id,
            "name": most_expensive.name,
            "price": most_expensive.price,
            "updated_at": most_expensive.updated_at.strftime("%Y-%m-%d %H:%M:%S") if most_expensive.updated_at else None,
        }

        return jsonify(response_data), 200
    else:
        return jsonify({"message": "No baked goods found."}), 404



if __name__ == '__main__':
    app.run(port=5555, debug=True)
