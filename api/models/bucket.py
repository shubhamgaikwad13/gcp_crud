from ...db import mongo_client as db
from datetime import datetime
from .user import User
from .base_model import BaseModel


class Bucket(BaseModel, db.Document):
    """Model for bucket objects"""

    name = db.StringField(unique=True)
    storageClass = db.StringField(default="Standard")
    locationType = db.StringField()
    location = db.StringField()
    uniformBucketLevelAccessEnabled = db.BooleanField()
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    created_by = db.ReferenceField(User, dbref=True)

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(name=id).first()


class BucketAcl(db.Document):
    """Model for BucketACL objects"""

    bucket = db.ReferenceField('Bucket', dbref=True)
    domain = db.StringField()
    email = db.StringField()
    entity = db.StringField()
    entityId = db.StringField()
    etag = db.StringField()
    id = db.StringField()
    role = db.StringField()
    selfLink = db.StringField()
