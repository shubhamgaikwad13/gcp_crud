from flask_restx import Api
from .bucket import bucket_api
from .auth import auth_api
from ...config import app_env


api = Api(
    version="1.0",
    title="API-V1",
    description="API using flask restplus",
    prefix="/api",

)

api.add_namespace(bucket_api)
api.add_namespace(auth_api)
