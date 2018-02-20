from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from dockblaster.database import db, BaseModel, Column
from dockblaster.extensions import login_manager


class User(UserMixin, BaseModel):
    """Model for the User table"""
    __tablename__ = 'users'
    user_id = Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = Column(db.String(64))
    last_name = Column(db.String(64))
    email = Column(db.String(120))
    password = Column(db.String(128))
    date_created = Column(db.DateTime)

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
        return str(self.user_id)

    @login_manager.user_loader
    def load_user(self):
        return User.query.get(int(id(self)))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

