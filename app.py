from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from admin import AdminClient, AdminDish, AdminCategory, AdminOrder
from config import Config
from models import Client, Dish, Order, Category

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
admin = Admin(app)
migrate = Migrate(app, db)

from views import *
admin.add_view(AdminClient(Client, db.session))
admin.add_view(AdminDish(Dish, db.session))
admin.add_view(AdminOrder(Order, db.session))
admin.add_view(AdminCategory(Category, db.session))

if __name__ == '__main__':
    app.run()
