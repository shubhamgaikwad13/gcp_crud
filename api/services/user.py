from ..models.user import User
from ..schemas.user import UserSchema
from .auth_service import firebase_auth
from flask import jsonify, request
from firebase_admin import auth


class UserService:
    model = User
    model_schema = UserSchema
    auth_firebase = firebase_auth

    @classmethod
    def add_user(cls, data: dict):
        """Creates a new user account and adds user details to the database"""

        try:
            schema = cls.model_schema(many=False)
            model_data = schema.load(data)

            firebase_user = cls.auth_firebase.sign_up(
                email=model_data.email, password=model_data.password
            )

            print("fb_user_id", firebase_user.uid)
            user = cls.model(**data, firebase_uid=firebase_user.uid)
            user.save()
            return model_data
        except Exception as e:
            return jsonify({"error": str(e)})

    @classmethod
    def login(cls, data: dict):
        """Authenticates the user and returns an access token"""

        try:
            login = cls.auth_firebase.auth.sign_in_with_email_and_password(**data)

            user = cls.auth_firebase.auth.get_account_info(login.get("idToken"))
            uid = login["localId"]
            # print("loginfbid", uid)
            mongo_user = cls.model.objects(firebase_uid=uid).first()

            custom_claims = {
                'user_id': str(mongo_user.id),
                "role": mongo_user.role
            }

            access_token = cls.auth_firebase.auth.create_custom_token(uid, custom_claims)

            return jsonify({"access_token": access_token, "refresh_token": login['refreshToken']})

        except Exception as e:
            raise Exception(str(e))

    @classmethod
    def get_user_id(cls):
        token = request.headers.get("Authorization").removeprefix("Bearer").strip()
        custom_token = cls.auth_firebase.auth.sign_in_with_custom_token(token)
        user = auth.verify_id_token(custom_token['idToken'])
        mongo_user = cls.model.fetch_by(firebase_uid=user['user_id']).first()

        return mongo_user.id
