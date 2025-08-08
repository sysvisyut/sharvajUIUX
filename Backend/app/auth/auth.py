from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os

auth_bp = Blueprint('auth', __name__)

def init_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        cred_path = current_app.config.get('FIREBASE_CREDENTIALS_PATH')
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            current_app.logger.warning("Firebase credentials not found. Auth bypass enabled.")

def auth_required(f):
    """Custom auth decorator with bypass option"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if auth bypass is enabled
        if current_app.config.get('BYPASS_AUTH', False):
            # In bypass mode, use a test user ID
            test_user = {'uid': 'test-user-123', 'email': 'test@example.com'}
            request.current_user = test_user
            return f(*args, **kwargs)
        
        # Normal JWT authentication
        try:
            token = request.headers.get('Authorization')
            if not token or not token.startswith('Bearer '):
                return jsonify({'error': 'Authorization token required'}), 401
            
            token = token.split(' ')[1]
            
            # For development, allow simple test tokens
            if current_app.config.get('DEBUG') and token == 'test-token':
                test_user = {'uid': 'test-user-123', 'email': 'test@example.com'}
                request.current_user = test_user
                return f(*args, **kwargs)
            
            # Verify Firebase ID token
            decoded_token = firebase_auth.verify_id_token(token)
            request.current_user = decoded_token
            return f(*args, **kwargs)
            
        except Exception as e:
            current_app.logger.error(f"Auth error: {str(e)}")
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function

def get_current_user():
    """Get current authenticated user"""
    return getattr(request, 'current_user', None)

@auth_bp.route('/verify', methods=['POST'])
@auth_required
def verify_token():
    """Verify authentication token"""
    user = get_current_user()
    return jsonify({
        'valid': True,
        'user': {
            'uid': user.get('uid'),
            'email': user.get('email', 'test@example.com')
        }
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint for Firebase authentication"""
    try:
        if current_app.config.get('BYPASS_AUTH', False):
            return jsonify({
                'message': 'Auth bypass enabled',
                'token': 'test-token',
                'user': {'uid': 'test-user-123', 'email': 'test@example.com'}
            })
        
        data = request.get_json()
        id_token = data.get('id_token')
        
        if not id_token:
            return jsonify({'error': 'Firebase ID token required'}), 400
        
        # Verify token with Firebase
        decoded_token = firebase_auth.verify_id_token(id_token)
        
        # Create custom JWT for backend
        access_token = create_access_token(identity=decoded_token['uid'])
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email')
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/test-login', methods=['POST'])
def test_login():
    """Test login for development/testing"""
    if not (current_app.config.get('DEBUG') or current_app.config.get('BYPASS_AUTH')):
        return jsonify({'error': 'Test login only available in debug mode or with auth bypass'}), 403

    return jsonify({
        'success': True,
        'data': {
            'message': 'Test login successful',
            'token': 'test-token',
            'user': {'uid': 'test-user-123', 'email': 'test@example.com'}
        }
    })
