from dockblaster.database import db, BaseModel, Column


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
    docking_job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    job_status_id = db.Column(db.Integer)
    date_started = db.Column(db.DateTime)
    job_type_id = db.Column(db.Integer)
    job_description = db.Column(db.String(500))

    def __init__(self, user_id, job_status_id, date_started, job_type_id, job_description):
        self.user_id = user_id
        self.job_status_id = job_status_id
        self.date_started = date_started
        self.job_type_id = job_type_id
        self.job_description = job_description


class Job_Type(BaseModel, db.Model):
    __tablename__ = 'job_types'
    job_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_name = db.Column(db.String(50))
    long_name = db.Column(db.String(80))

    def __init__(self, short_name, long_name):
        self.short_name = short_name
        self.long_name = long_name