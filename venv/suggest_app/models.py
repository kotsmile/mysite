from suggest_app import db
from suggest_app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import url_for, redirect


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Admin {}>'.format(self.login)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ActivityLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    activity_level = db.Column(db.Float)


class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    days = db.Column(db.Integer)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    percent = db.Column(db.Float)


class EqConf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(64))
    const = db.Column(db.Float)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    age = db.Column(db.Float)


categories = db.Table('categories_items',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    gramm = db.Column(db.Float)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrate = db.Column(db.Float)
    link = db.Column(db.String(64))
    categories = db.relationship('Category', secondary=categories,
                                 backref=db.backref('items', lazy='dynamic'))
    item_group_id = db.Column(db.Integer, db.ForeignKey('item_group.id'))

    def __repr__(self):
        return self.name

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return self.name


class ItemGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    percent = db.Column(db.Float)
    addresses = db.relationship('Item', backref='item_group',
                                lazy='dynamic')
    def __repr__(self):
        return self.name



class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


class LoginModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('create_suggest'))
