import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
from ...firebaseadminConfig import fb_admin_config
from ...fbconfig import fb_config


class Firebase:

    def __init__(self):
        self.cred = credentials.Certificate(fb_admin_config)
        self.firebase_admin = firebase_admin.initialize_app(self.cred)
        self.firebase = pyrebase.initialize_app(fb_config)
        self.auth = self.firebase.auth()

    def sign_up(self, **kwargs):
        try:
            return auth.create_user(**kwargs)
        except Exception as e:
            raise Exception(str(e))


firebase_auth = Firebase()
