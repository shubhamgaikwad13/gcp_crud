from marshmallow_mongoengine import ModelSchema, fields
from ..models.bucket import Bucket, BucketAcl


class BucketSchema(ModelSchema):
    class Meta:
        model = Bucket


class BucketAclSchema(ModelSchema):
    class Meta:
        model = BucketAcl
