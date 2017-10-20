import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BASEDIR = basedir
    STATIC_DIR = os.path.join(BASEDIR, 'static')
    YMS_PRODUCTS_PER_PAGE = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'data-develop.sqlite')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'data-test.sqlite')
    FAKE_PRODUCTS_COUNT = 10


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
    YMS_PRODUCTS_PER_PAGE = 15


configs = {
    'default': DevConfig,

    'develop': DevConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}
