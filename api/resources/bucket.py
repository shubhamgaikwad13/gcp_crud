from flask_restx import Resource, Namespace, fields
from flask import request, jsonify
from ..utils.token_required import token_required

from ..services.bucket import BucketService, BucketAclService
bucket_api = Namespace("bucket", description="Operations related to gcp buckets", path="/bucket")

bucket_model = bucket_api.model('Bucket',
                                {
                                    "uniformBucketLevelAccessEnabled": fields.Boolean(),
                                    "name": fields.String('The bucket name'),
                                    "locationType": fields.String('The bucket location type'),
                                    "location": fields.String('The bucket location'),
                                    "storageClass": fields.String('The bucket storage class')
                                })

bucket_delete_parser = bucket_api.parser()
bucket_delete_parser.add_argument('name', type=str, required=True, help='The bucket name')


@bucket_api.route("/")
class Bucket(Resource):

    @classmethod
    def get(self):
        try:
            return jsonify({"buckets": BucketService.list_buckets()})
        except Exception as e:
            return jsonify({"error": str(e)})

    @bucket_api.expect(bucket_model)
    @token_required(roles=['STORAGE_ADMIN'])
    def post(self):
        try:
            return jsonify({"user": BucketService.create_bucket(bucket_api.payload)})
        except Exception as e:
            return jsonify({"error": str(e)})

    # @bucket_api.expect(bucket_delete_parser)
    @bucket_api.param('name', type=str, description='The bucket name')
    @token_required(roles=['STORAGE_ADMIN'])
    def delete(self):
        args = request.args.to_dict()

        # return BucketService.delete_bucket(bucket_delete_parser.parse_args())
        return jsonify({"message": BucketService.delete_bucket(args.get('name'))})


@bucket_api.route("/acls")
class BucketAcl(Resource):

    @bucket_api.param('name', type=str, description='The bucket name')
    def get(self):
        args = request.args.to_dict()

        return BucketAclService.list_bucket_acl(args.get('name'))
