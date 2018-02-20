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
    docking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    job_status_id = db.Column(db.Integer)
    date_started = db.Column(db.DateTime)

    def __init__(self, user_id, job_status_id, date_started):
        self.user_id = user_id
        self.job_status_id = job_status_id
        self.date_started = date_started