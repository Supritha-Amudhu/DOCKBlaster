import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': 'blasteruser',
    'pw': '',
    'db': 'blaster',
    'host': 'mem.cluster.ucsf.bkslab.org',
    'port': '5432',
    #'port': '6543',
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DOCK-Blaster'
    SESSION_TYPE = 'filesystem'
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://blasteruser:@localhost:6543/blaster"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://blasteruser:@mem.cluster.ucsf.bkslab.org:5432/blaster"
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'DOCKBlaster/Files'
    DEBUG = True



class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = True
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'DOCKBlaster.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    DEBUG_TB_ENABLED = True
    UPLOAD_FOLDER = '/Users/supritha/Workspace/PycharmProjects/DOCKBlaster/Files'
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing