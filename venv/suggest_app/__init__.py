from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.menu import MenuLink

from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object(Config)

# app.config['ENV'] = 'development'
app.config['DEBUG'] = False
# app.config['TESTING'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


login = LoginManager(app)

from suggest_app import routes, models

admin = Admin(app, index_view=models.AdminView())
admin.add_link(MenuLink(name='Выйти', category='', url='/logout'))
admin.add_view(models.LoginModelView(models.Item, db.session))
admin.add_view(models.LoginModelView(models.Category, db.session))
admin.add_view(models.LoginModelView(models.ItemGroup, db.session))
admin.add_view(models.LoginModelView(models.MealType, db.session))
admin.add_view(models.LoginModelView(models.Combination, db.session))
admin.add_view(models.LoginModelView(models.Goal, db.session))
admin.add_view(models.LoginModelView(models.ActivityLevel, db.session))
admin.add_view(models.LoginModelView(models.EqConf, db.session))
