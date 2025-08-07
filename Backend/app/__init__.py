from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from config.config import config
from app.models.database import Database
import os

def create_app(config_name=None):
    """Create Flask application factory"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, origins=['http://localhost:3000', 'http://localhost:8080'])  # Add your frontend URLs
    jwt = JWTManager(app)
    
    # Initialize MongoDB
    try:
        Database.initialize(app.config['MONGO_URI'])
        app.logger.info(f"Connected to MongoDB: {app.config['MONGO_URI']}")
    except Exception as e:
        app.logger.error(f"Failed to connect to MongoDB: {str(e)}")
    
    # Register blueprints
    from app.auth.auth import auth_bp
    from app.api.routes import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'config': config_name,
            'auth_bypass': app.config.get('BYPASS_AUTH', False)
        }
    
    # Root endpoint
    @app.route('/')
    def root():
        return {
            'message': 'Credit Score Analysis API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/auth',
                'api': '/api',
                'health': '/health'
            }
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden'}, 403
    
    return app
