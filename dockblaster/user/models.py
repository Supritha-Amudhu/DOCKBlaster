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
    admin = db.Column(db.Boolean)
    deleted = db.Column(db.Boolean)
    api_key = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, password, date_created, admin = False, deleted = False, api_key = "test"):
        super(User, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.date_created = date_created
        self.admin = admin
        self.deleted = deleted
        self.api_key = api_key

    def __repr__(self):
        return "<User: {}".format(self.first_name)

    def get_id(self):
        return unicode(self.user_id)

    def get_username(self):
        return self.first_name

    def is_admin(self):
        return self.admin

    def is_active_user(self):
        return not self.deleted

    def get_email(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_api_key(self, api_key):
        return self.api_key

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if not api_key:
        api_key = request.form.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user