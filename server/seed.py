from faker import Faker
from app import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

def delete_data():
    db.session.query(RestaurantPizza).delete()
    db.session.query(Restaurant).delete()
    db.session.query(Pizza).delete()
    db.session.commit()

def create_restaurants(num_restaurants):
    for _ in range(num_restaurants):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        db.session.add(restaurant)
    db.session.commit()

def create_pizzas(num_pizzas):
    for _ in range(num_pizzas):
        pizza = Pizza(
            name=fake.word().capitalize(),
            ingredients=', '.join(fake.words(5))
        )
        db.session.add(pizza)
    db.session.commit()

def create_restaurant_pizzas(num_associations, num_restaurants, num_pizzas):
    for _ in range(num_associations):
        restaurant_id = fake.random_int(min=1, max=num_restaurants)
        pizza_id = fake.random_int(min=1, max=num_pizzas)
        price = fake.pyfloat(min_value=1, max_value=30, right_digits=2)
        association = RestaurantPizza(
            restaurant_id=restaurant_id,
            pizza_id=pizza_id,
            price=price
        )
        db.session.add(association)
    db.session.commit()

if __name__ == '__main__':
    num_restaurants = 10
    num_pizzas = 20
    num_associations = 50

    delete_data()
    create_restaurants(num_restaurants)
    create_pizzas(num_pizzas)
    create_restaurant_pizzas(num_associations, num_restaurants, num_pizzas)

    print("Database seeded successfully!")
