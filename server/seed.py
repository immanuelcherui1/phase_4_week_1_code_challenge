from faker import Faker
from app import db, Restaurant, Pizza, RestaurantPizza
from random import randint, choice as rc

from app import app

fake = Faker()


with app.app_context():
    # Delete existing records
    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()
   
    # Seed restaurants
    restaurants = []
    for _ in range(10):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        restaurants.append(restaurant)
    db.session.add_all(restaurants)

    # Seed pizzas
    pizzas = []
    for _ in range(20):
        pizza = Pizza(
            name=fake.word().capitalize(),
            ingredients=', '.join(fake.words(5))
        )
        pizzas.append(pizza)
    db.session.add_all(pizzas)

    # Seed restaurant-pizza associations
    restaurantpizzas = []
    for _ in range(50):
        restaurant_id = fake.random_int(min=1, max=10)
        pizza_id = fake.random_int(min=1, max=20)
        price = fake.pyfloat(min_value=1, max_value=30, right_digits=2)
        association = RestaurantPizza(
            restaurant_id=restaurant_id,
            pizza_id=pizza_id,
            price=price
        )
        db.session.add(association)
    db.session.commit()

    print("Database seeded successfully!")
