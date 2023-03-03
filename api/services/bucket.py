from ..resources.storage import storage_service
from flask import jsonify
from ...settings import PROJECT_ID
from ..models.bucket import Bucket, BucketAcl
from ..schemas.bucket import BucketSchema, BucketAclSchema
from ..utils.constant import *
import json


class BucketService:
    model = Bucket
    model_schema = BucketSchema

    @classmethod
    def list_buckets(cls):
        """Gets list of all the buckets in the project"""
        try:
            # buckets = storage_service.buckets().list(project=PROJECT_ID).execute()['items']
            buckets = cls.model.objects()
            return jsonify({"buckets": cls.model_schema().dump(obj=buckets, many=True)})
        except Exception as e:
            return jsonify({"error": str(e)})

    @classmethod
    def create_bucket(cls, data:dict):
        """Creates a new gcp bucket in project"""

        try:
            schema = cls.model_schema(many=False)
            model_data = schema.load(data)

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
            print(data)
            cls.model(**data).save()

            return jsonify({"message": response})

        except Exception as e:
            return jsonify({"error": str(e)})

    @classmethod
    def delete_bucket(cls, bucket_name):
        """Deletes an existing empty bucket from project"""

        try:
            response = storage_service.buckets().delete(bucket=bucket_name).execute()
            cls.model.objects(name=bucket_name).delete()
            if not response:
                return jsonify({"message": BUCKET_DELETED_SUCCESSFULLY})

        except Exception as e:
            return jsonify({"error": str(e)})
            # return jsonify({"error": json.loads(e.content)['error']['message']})


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
