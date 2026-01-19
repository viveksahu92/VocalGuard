"""
VocalGuard Authentication Module
JWT-based authentication with bcrypt password hashing
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'vocalguard-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DAYS = 7


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def generate_token(user_id: int, email: str) -> str:
    """Generate a JWT token for a user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')


def get_token_from_request():
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    # Expected format: "Bearer <token>"
    parts = auth_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]


def require_auth(f):
    """Decorator to protect routes with authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({'error': 'Authentication required', 'code': 'NO_TOKEN'}), 401
        
        try:
            payload = decode_token(token)
            request.user_id = payload['user_id']
            request.user_email = payload['email']
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e), 'code': 'INVALID_TOKEN'}), 401
    
    return decorated_function


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    if not any(c.isdigit() for c in password):
        return False, 'Password must contain at least one number'
    
    if not any(c.isalpha() for c in password):
        return False, 'Password must contain at least one letter'
    
    return True, ''


def verify_google_token(token: str) -> dict:
    """
    Verify Google ID token and extract user information
    For development, this accepts any token and extracts email
    In production, use Google's official verification library
    """
    try:
        # For development/demo: Simple JWT decode without verification
        # WARNING: In production, use google.oauth2.id_token.verify_oauth2_token()
        import json
        import base64
        
        # Decode JWT payload (without verification - FOR DEMO ONLY)
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError('Invalid token format')
        
        # Decode payload
        payload_encoded = parts[1]
        # Add padding if needed
        padding = 4 - len(payload_encoded) % 4
        if padding != 4:
            payload_encoded += '=' * padding
        
        payload_bytes = base64.urlsafe_b64decode(payload_encoded)
        payload = json.loads(payload_bytes)
        
        # Extract user info
        return {
            'success': True,
            'email': payload.get('email'),
            'name': payload.get('name'),
            'google_id': payload.get('sub'),  # Google user ID
            'picture': payload.get('picture')
        }
        
    except Exception as e:
        print(f"Google token verification error: {e}")
        return {
            'success': False,
            'error': 'Invalid Google token'
        }
