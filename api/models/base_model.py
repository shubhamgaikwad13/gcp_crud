

class BaseModel:
    @classmethod
    def fetch_by_id(cls, _id):
        return cls.objects(id=_id).first()

    @classmethod
    def fetch_by(cls, **kwargs):
        return cls.objects(**kwargs)

