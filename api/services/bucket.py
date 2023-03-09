from ..resources.storage import storage_service
from flask import jsonify
from ...settings import PROJECT_ID
from ..models.bucket import Bucket, BucketAcl
from ..schemas.bucket import BucketSchema, BucketAclSchema
from ..utils.constant import *
from ..exceptions import (ApiException,
                          BucketAlreadyCreatedException,
                          BucketDoesNotExistException,
                          ValidationException,
                          BucketAlreadyExistsException
                        )
from marshmallow.exceptions import ValidationError
from googleapiclient.errors import HttpError
from http import HTTPStatus
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mongoengine.queryset.visitor import Q


class BucketService:
    model = Bucket
    model_schema = BucketSchema

    @classmethod
    def list_buckets(cls, **kwargs):
        """Gets list of all the buckets in the project"""

        try:
            # buckets = storage_service.buckets().list(project=PROJECT_ID).execute()['items']
            buckets = cls.model.objects()
            print(kwargs)
            if kwargs.get('location'):
                buckets = buckets.filter(location=kwargs.get('location'))

            buckets = cls.model_schema().dump(obj=buckets, many=True)

            return buckets
        except Exception:
            raise ApiException(FETCH_ERROR)

    @classmethod
    def create_bucket(cls, data: dict):
        """Creates a new gcp bucket in project"""

        try:
            schema = cls.model_schema(many=False)
            model_data = schema.load(data)

            bucket = cls.model.get_by_id(model_data.name)

            if bucket:
                raise BucketAlreadyCreatedException()

            response = storage_service.buckets().insert(
                project=PROJECT_ID,
                body={
                    "iamConfiguration": {
                        "uniformBucketLevelAccess": {
                            "enabled": model_data.uniformBucketLevelAccessEnabled
                        }
                    },
                    "name": model_data.name,
                    "locationType": model_data.locationType,
                    "location": model_data.location,
                    "storageClass": model_data.storageClass
                }).execute()

            if response:
                bucket = cls.model(**data).save()
                return bucket

        except ValidationError as e:
            print('this: ', e)
            raise ValidationException(e)
        except HttpError as e:
            if e.status_code == HTTPStatus.CONFLICT:
                raise BucketAlreadyExistsException()
            raise ApiException(e.reason)

    @classmethod
    def delete_bucket(cls, bucket_name, recursive=False):
        """Deletes an existing empty bucket from project"""

        bucket = cls.model.get_by_id(bucket_name)

        if not bucket:
            raise BucketDoesNotExistException()

        try:
            if bucket and recursive == 'true':
                # Deletes all objects from the bucket recursively
                objects = storage_service.objects().list(bucket=bucket_name).execute()

                if objects.get('items'):
                    for item in objects['items']:
                        storage_service.objects().delete(bucket=bucket_name, object=item['name']).execute()

            response = storage_service.buckets().delete(bucket=bucket_name).execute()

            is_deleted = cls.model.objects(name=bucket_name).delete()

            return is_deleted

        except Exception as e:
            print(e)
            raise ApiException(e)

    @classmethod
    def get_bucket(cls, bucket_name):
        """Gets bucket details for the specified bucket"""

        try:
            bucket = cls.model.get_by_id(bucket_name)
            bucket = cls.model_schema().dump(bucket)

            return bucket
        except Exception:
            raise ApiException(FETCH_ERROR)

    @classmethod
    def fetch_by_search_keyword(cls, search_keyword):
        if search_keyword:
            query = cls.model.objects(Q(name__icontains=search_keyword) | Q(storageClass__icontains=search_keyword))

        buckets = cls.model_schema().dump(query, many=True)
        return buckets


class BucketExportService:
    @classmethod
    def export_to_csv(cls):
        buckets = BucketService.list_buckets()
        # print(type(buckets), buckets)
        dataframe = pd.DataFrame(buckets)

        dataframe.to_csv('buckets.csv')

    @classmethod
    def export_to_excel(cls):
        buckets = BucketService.list_buckets()

        dataframe = pd.DataFrame(buckets)

        dataframe.to_excel('buckets.xlsx')

    @classmethod
    def export_to_pdf(cls):
        buckets = BucketService.list_buckets()

        dataframe = pd.DataFrame(buckets)

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('tight')
        ax.axis('off')
        the_table = ax.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center')

        pp = PdfPages("buckets.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()



class BucketAclService:
    model = BucketAcl
    model_schema = BucketAclSchema

    @classmethod
    def list_bucket_acl(cls, bucket_name):
        """Retrieves acl entries on a specified bucket"""
        try:
            response = storage_service.bucketAccessControls().list(bucket=bucket_name).execute()

            print(response)

            return jsonify({"acls": response})
        except Exception as e:
            return jsonify({"error": str(e)})
