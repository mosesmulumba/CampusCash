from functools import wraps
from flask_jwt_extended import get_jwt_identity , verify_jwt_in_request , get_jwt
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        
        if not claims.get('is_admin' , False):
            return {'msg': "Admin access required"} , 403
        
        return f(*args , **kwargs)
    
    return decorated_function