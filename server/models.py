from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-pizzas',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String)

    pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    
    def __repr__(self):
        return f'<Restaurant {self.name}, ${self.address if self.address else ""}>'

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurants',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ingredients = db.Column(db.String)

    restaurants = db.relationship("RestaurantPizza", back_populates="pizza")

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients if self.ingredients else ""}>'
    

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurantpizzas'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30.")
        return price
    
    restaurant = db.relationship("Restaurant", back_populates="pizzas")
    pizza = db.relationship("Pizza", back_populates="restaurants")
    
    def __repr__(self):
        return f'<RestaurantPizza {self.restaurant_id}, ${self.price}, ${self.pizza_id}>'
