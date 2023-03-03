from flask_restx import Resource, Namespace, fields, reqparse
from flask import request, jsonify
from ..services.user import UserService
from ..utils.token_required import token_required

authorizations = {
        "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Bearer"},
}

auth_api = Namespace("auth", description="Operations related to User Authentication", path="/auth", authorizations=authorizations)

auth_model = auth_api.model('Auth', {
    "first_name": fields.String("User's first name"),
    "last_name": fields.String("User's last name"),
    "email": fields.String("User's email"),
    "role": fields.String("User's role['STORAGE_ADMIN', 'STORAGE_VIEWER']"),
    "password": fields.String("User's password")
})


login_parser = reqparse.RequestParser()
login_parser.add_argument(
    "email", type=str, required=True, help="Your email", location="form"
)
login_parser.add_argument(
    "password", type=str, required=True, help="Your password", location="form"
)


@auth_api.route("/signup")
class SignUp(Resource):

    @auth_api.expect(auth_model)
    def post(self):
        user_info = request.json

        result = UserService.add_user(user_info)
        print(result.__dict__)
        return jsonify({"message": "User added successfully."})


@auth_api.route("/login")
class Login(Resource):

    @auth_api.expect(login_parser)
    def post(self):
        try:
            user_credentials = request.form.to_dict()

            token = UserService.login(user_credentials)
        except Exception as e:
            return jsonify({"error": str(e)})

        return token


@auth_api.route("/demo", )
# @auth_api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class ProtectedRoute(Resource):

    @token_required(roles=['STORAGE_ADMIN'])
    def get(self):
        return "Hello"
