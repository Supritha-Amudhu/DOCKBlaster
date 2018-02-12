from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super(BaseModel, self).__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class User(BaseModel, db.Model):
    """Model for the User table"""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime)

    def __init__(self, user_id, username, email, password_hash, date_created):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.date_created = date_created

    def __repr__(self):
        return "<User: {}".format(self.username)


class Job_Status(BaseModel, db.Model):
    """Model for Job statuses"""
    __tablename__ = 'job_status'
    job_status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_status_name = db.Column(db.String(64))

    def __init__(self, job_status_id, job_status_name):
        self.job_status_id = job_status_id
        self.job_status_name = job_status_name


class Docking_Job(BaseModel, db.Model):
    """Model for a Job table that records data about docking"""
    __tablename__ = 'docking_jobs'
    docking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    job_status_id = db.Column(db.Integer)
    date_started = db.Column(db.DateTime)

    def __init__(self, docking_id, user_id, job_status_id, date_started):
        self.docking_id = docking_id
        self.user_id = user_id
        self.job_status_id = job_status_id
        self.date_started = date_started


