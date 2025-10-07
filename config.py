class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Jones22*@localhost/Mechanic_API_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False