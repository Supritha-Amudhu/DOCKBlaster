import os
basedir = os.path.abspath(os.path.dirname(__file__))
from os.path import expanduser


POSTGRES = {
    'user': 'blasteruser',
    'pw': '',
    'db': 'blaster',
    'host': 'mem.cluster.ucsf.bkslab.org',
    'port': '5432',
}


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'DOCK-Blaster'
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://blasteruser:@mem.cluster.ucsf.bkslab.org:5432/blaster"
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_POOL_TIMEOUT = 10
    UPLOAD_FOLDER = '/nfs/ex7/blaster/jobs/'
    PARSE_FOLDER = '/nfs/ex7/blaster/templates/'
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
    DB_NAME = 'dockblaster.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    DEBUG_TB_ENABLED = True
    UPLOAD_FOLDER = expanduser("~") + '/DOCKBlaster/jobs/'
    PARSE_FOLDER = expanduser("~") + '/DOCKBlaster/templates/'
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_DATABASE_URI="postgresql://localhost/dockblaster"


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
