from suggest_app import db
from suggest_app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class Admin(UserMixin, db.Model):
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
    return Admin.query.get(int(id))