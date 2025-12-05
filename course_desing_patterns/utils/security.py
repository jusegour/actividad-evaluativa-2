from functools import wraps
from flask import request

# Idealmente, esto vendría de variables de entorno, no hardcoded.
VALID_TOKEN = 'abcd12345' 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return {'message': 'Unauthorized: Access token not found'}, 401
            
        if token != VALID_TOKEN:
            return {'message': 'Unauthorized: Invalid token'}, 401
            
        return f(*args, **kwargs)
    return decorated