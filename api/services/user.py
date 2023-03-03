from ..models.user import User
from ..schemas.user import UserSchema
from .auth_service import firebase_auth
from flask import jsonify


class UserService:
    model = User
    model_schema = UserSchema
    auth_firebase = firebase_auth

    @classmethod
    def add_user(cls, data: dict):
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
        try:
            login = cls.auth_firebase.auth.sign_in_with_email_and_password(**data)

            user = cls.auth_firebase.auth.get_account_info(login.get("idToken"))
            uid = login["localId"]
            # print("loginfbid", uid)
            mongo_user = cls.model.objects(firebase_uid=uid).first()

            custom_claims = {
                "role": mongo_user.role
            }

            access_token = cls.auth_firebase.auth.create_custom_token(uid, custom_claims)

            return jsonify({"access_token": access_token, "refresh_token": login['refreshToken']})

        except Exception as e:
            raise Exception(str(e))
