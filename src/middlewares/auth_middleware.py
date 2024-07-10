import os

import jwt
from flask import request, g

from src.http.exception.exception import UnauthorizedException, ForbiddenException


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
                    raise UnauthorizedException("Token Expired")
                except jwt.InvalidTokenError:
                    raise UnauthorizedException("Invalid Token")
            else:
                raise UnauthorizedException("Authorization token is missing")

            if len(roles) >= 0:
                if not g.get('user'):
                    raise UnauthorizedException("Authorization token is missing")
                user_roles = g.user.get('role', [])
                if not any(role in user_roles for role in roles):
                    raise ForbiddenException("Permission Denied")

            return f(*args, **kwargs)

        return decorated_function

    return decorator
