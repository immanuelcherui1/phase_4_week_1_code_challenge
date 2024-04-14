#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h2>PIZZA RESTAURANTS</h2>'

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        restaurant_list.append(restaurant_data)
    return jsonify(restaurant_list)

@app.route('/restaurants/<int:id>', methods= ['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id==id).first()

    if restaurant:
        if request.method=='GET':
            pizzas = [{"id": rp.pizza.id, "name": rp.pizza.name, "ingredients": rp.pizza.ingredients} for rp in restaurant.pizzas]
            restaurant_data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": pizzas
            }
            return jsonify(restaurant_data)
    
        elif request.method == 'DELETE':
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
    
    else:
        return jsonify({"error": "Restaurant not found"}), 404
    
@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []
    for pizza in pizzas:
        pizza_data = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }
        pizza_list.append(pizza_data)
    return jsonify(pizza_list)

@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizzas():
    pizza_id=request.form.get("pizza_id")
    restaurant_id=request.form.get("restaurant_id")
    price=request.form.get("price")


    if not (pizza_id and restaurant_id and price):
        return jsonify({"error": "Missing required data"}), 400

    # Converting data types and validate
    try:
        pizza_id = int(pizza_id)
        restaurant_id = int(restaurant_id)
        price = float(price)
    except ValueError:
        return jsonify({"error": "Invalid data type for pizza_id, restaurant_id, or price"}), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not (pizza and restaurant):
        return jsonify({"error": "Pizza or restaurant not found"}), 404

    restaurant_pizza = RestaurantPizza(
        pizza_id=pizza_id,
        restaurant_id=restaurant_id,
        price=price
    )

    db.session.add(restaurant_pizza)
    db.session.commit()
    
    restaurant_pizza_dict= restaurant_pizza.to_dict()
    return jsonify(restaurant_pizza_dict), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
