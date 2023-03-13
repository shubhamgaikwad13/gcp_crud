from marshmallow_mongoengine import ModelSchema, fields
from ..models.bucket import Bucket, BucketAcl


class BucketSchema(ModelSchema):
    class Meta:
        model = Bucket

    created_by = fields.Nested('UserSchema', many=False, load_only=True, allow_none=True)


class BucketAclSchema(ModelSchema):
    class Meta:
        model = BucketAcl
