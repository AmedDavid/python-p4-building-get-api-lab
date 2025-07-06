#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

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
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict(rules=("-baked_goods.bakery", "baked_goods")) for bakery in bakeries]
    return make_response(jsonify(bakeries_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_dict = bakery.to_dict(rules=("-baked_goods.bakery", "baked_goods"))
    return make_response(jsonify(bakery_dict), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [bg.to_dict(rules=("-bakery.baked_goods", "bakery")) for bg in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bg:
        bg_dict = bg.to_dict(rules=("-bakery.baked_goods", "bakery"))
        return make_response(jsonify(bg_dict), 200)
    else:
        return make_response(jsonify({}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
