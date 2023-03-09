from functools import wraps
from flask import request
from firebase_admin import auth
from ..services.auth_service import firebase_auth
from ..models.user import User
from ..exceptions import NoTokenException, AuthException, InvalidTokenException


def token_required(roles=list(User.roles.keys())):
    """Decorator to require login and role based access control"""

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if not request.headers.get('Authorization'):
                # return {'message': 'No token provided'}, 400
                raise NoTokenException()

            try:
                # token = request.headers.get('Authorization')[7:]
                token = request.headers.get("Authorization").removeprefix("Bearer").strip()
                # print(token)
                custom_token = firebase_auth.auth.sign_in_with_custom_token(token)
                user = auth.verify_id_token(custom_token['idToken'])

            except Exception as e:
                raise InvalidTokenException()

            if user.get('role') not in roles:
                raise AuthException()
            return func(*args, **kwargs)
        return wrap

    return decorator
