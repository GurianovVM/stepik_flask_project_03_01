from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

order_dish = db.Table('order_dishes',
                      db.Column('order_id',db.Integer, db.ForeignKey('orders.id')),
                      db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
                      )

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='')
    password = db.Column(db.String(32))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15), default='')
    address = db.Column(db.String(50), default='')
    orders = db.relationship('Order')


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category')
    orders = db.relationship('Order', secondary=order_dish, back_populates='dishes')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dishes = db.relationship('Dish')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    cash = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), default='')
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client')
    dishes = db.relation('Dish', secondary=order_dish, back_populates='orders')
