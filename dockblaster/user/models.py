from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from dockblaster.database import db, BaseModel, Column
from dockblaster.extensions import login_manager


class User(UserMixin, BaseModel):
    """Model for the User table"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    date_created = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, email, password, date_created):
        super(User, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.date_created = date_created

    def __repr__(self):
        return "<User: {}".format(self.first_name)

    def get_id(self):
        return unicode(self.user_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)