class Config(object):
    DEBUG = False
    TESTING = False
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = 'localhost'
    PORT = 3306
    DBNAME = 'test'
    # SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:123456@127.0.0.1:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True