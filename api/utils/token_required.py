from functools import wraps
from flask import request
from firebase_admin import auth
from ..services.auth_service import firebase_auth
from ..models.user import User


def token_required(roles=list(User.roles.keys())):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if not request.headers.get('Authorization'):
                return {'message': 'No token provided'}, 400

            try:
                token = request.headers.get('Authorization')[7:]

                custom_token = firebase_auth.auth.sign_in_with_custom_token(token)
                user = auth.verify_id_token(custom_token['idToken'])

                if user.get('role') not in roles:
                    raise Exception("Unauthorized Access.")
            except Exception as e:
                return {'message':'Invalid token provided.', "error": str(e)}, 400
            return func(*args, **kwargs)
        return wrap

    return decorator
