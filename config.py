import os

class Config:
    # Add any common configurations here
    pass

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URL = os.getenv('DEVELOPMENT_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = os.getenv('TEST_DATABASE_URL')

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URL = os.getenv('STAGING_DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv('PRODUCTION_DATABASE_URL')

configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}