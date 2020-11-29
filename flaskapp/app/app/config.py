import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:

    API_PREFIX = "/api"
    TESTING = False
    DEBUG = False
    RESTPLUS_VALIDATE = True
    OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 3600
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ghtPrfgvbfd0W987hbnaXsweG'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = "development"
    # celery here
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    # celery here
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-prod.sqlite')


config = {
    'development': DevConfig,
    'testing': TestingConfig,
    'production': ProdConfig,

    'default': DevConfig
}
