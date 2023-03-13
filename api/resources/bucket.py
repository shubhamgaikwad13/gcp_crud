from flask_restx import Resource, Namespace, fields
from flask import request
from ..utils.token_required import token_required
from ..utils.common import json_response
from ..utils.constant import *
from ..services.bucket import BucketService, BucketAclService, BucketExportService

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
# bucket_delete_parser.add_argument('')


@bucket_api.route("/")
class BucketList(Resource):

    @classmethod
    def get(cls):
        args = request.args.to_dict()

        buckets = BucketService.list_buckets(**args)

        page = int(args.get('page', 1))
        per_page = int(args.get('per_page', 10))

        start = (page - 1) * per_page
        end = start + per_page

        paginated_buckets = buckets[start:end]

        return json_response(data=paginated_buckets, data_key='buckets')

    @bucket_api.expect(bucket_model)
    @token_required(roles=['STORAGE_ADMIN'])
    def post(self):
        return json_response(message=BUCKET_CREATED_SUCCESSFULLY, data=BucketService.create_bucket(bucket_api.payload))

    # @bucket_api.param('name', type=str, description='The bucket name')
    # @token_required(roles=['STORAGE_ADMIN'])
    # def delete(self):
    #     args = request.args.to_dict()
    #
    #     response = BucketService.delete_bucket(args.get('name'), args.get('recursive'))
    #
    #     if response:
    #         return json_response(message=BUCKET_DELETED_SUCCESSFULLY)


@bucket_api.route("/<bucket_name>")
class Bucket(Resource):

    @classmethod
    def get(cls, bucket_name):
        # print(bucket_name)
        bucket = BucketService.get_bucket(bucket_name)
        return json_response(data=bucket, data_key='bucket')

    @token_required(roles=['STORAGE_ADMIN'])
    @bucket_api.expect(bucket_delete_parser)
    def delete(self, bucket_name):
        args = request.args.to_dict()

        response = BucketService.delete_bucket(bucket_name, args.get('recursive'))

        if response:
            return json_response(message=BUCKET_DELETED_SUCCESSFULLY)


@bucket_api.route("/export/<file_format>")
class BucketExport(Resource):
    @classmethod
    def post(cls, file_format):
        if file_format == 'csv':
            BucketExportService.export_to_csv()
        if file_format == 'excel':
            BucketExportService.export_to_excel()
        if file_format == 'pdf':
            BucketExportService.export_to_pdf()


@bucket_api.route("/search/")
class BucketSearch(Resource):
    @classmethod
    def get(cls):
        args = request.args.to_dict()

        search_keyword = args.get('search')
        print(search_keyword)
        return BucketService.fetch_by_search_keyword(search_keyword)


# @bucket_api.route("/filter/")
# class BucketFilter(Resource):
#
#     def get(self):
#         args = request.args.to_dict()
#
#         filter_by = args.get('filter_by')


@bucket_api.route("/acls")
class BucketAcl(Resource):

    @bucket_api.param('name', type=str, description='The bucket name')
    def get(self):
        args = request.args.to_dict()

        return BucketAclService.list_bucket_acl(args.get('name'))
