import os

import jwt
from flask import request, jsonify, g


def auth_required(*roles):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            request_token = request.headers.get('Authorization')
            jwt_secret = os.getenv('JWT_SECRET', 'secret')

            if request_token and request_token.startswith('Bearer '):
                try:
                    token = request_token.split(' ')[1]
                    payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
                    g.user = payload
                except jwt.ExpiredSignatureError:
                    return {'message': 'Token has expired'}, 401
                except jwt.InvalidTokenError:
                    return {'message': 'Invalid token'}, 401
            else:
                g.user = None
                return {'message': 'Authorization token is missing'}, 401

            if roles:
                if not g.get('user'):
                    return {'message': 'Authorization token is missing'}, 401
                user_roles = g.user.get('role', [])
                if not any(role in user_roles for role in roles):
                    return {'message': 'Permission denied'}, 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator
