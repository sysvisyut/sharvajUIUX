import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/credit_score_db'
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH')
    
    # External APIs
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPEN_ROUTER_MODEL = os.environ.get('OPEN_ROUTER_MODEL') or 'meta-llama/llama-3.3-70b-instruct:free'
    OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
    
    # ML Model Configuration
    ML_MODEL_URL = os.environ.get('ML_MODEL_URL') or 'http://localhost:8000'
    ML_MODEL_LOCAL = os.environ.get('ML_MODEL_LOCAL', 'True').lower() == 'true'
    
    # Testing Configuration
    BYPASS_AUTH = os.environ.get('BYPASS_AUTH', 'False').lower() == 'true'
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    BYPASS_AUTH = True  # Allow auth bypass in development
    MONGO_URI = 'mongodb://localhost:27017/credit_score_dev'

class TestingConfig(Config):
    TESTING = True
    BYPASS_AUTH = True
    MONGO_URI = 'mongodb://localhost:27017/credit_score_test'

class ProductionConfig(Config):
    DEBUG = False
    BYPASS_AUTH = False  # Never bypass auth in production
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
