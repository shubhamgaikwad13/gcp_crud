from ...db import mongo_client as db
from datetime import datetime


class User(db.Document):
    roles = {
        "STORAGE_ADMIN": ("create", "read", "update", "delete"),
        "STORAGE_VIEWER": ("read", )
    }

    first_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField(unique=True, required=True)
    role = db.StringField()
    password = db.StringField(required=True)
    is_active = db.BooleanField(default=False)
    created_at = db.DateTimeField(datetime.utcnow)
    updated_at = db.DateTimeField(datetime.utcnow)
    firebase_uid = db.StringField()
