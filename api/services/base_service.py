from bson.objectid import ObjectId


class BaseService:
    model = None
    model_schema = None

    @classmethod
    def fetch_by_id(cls, _id):
        data = cls.model.fetch_by_id(ObjectId(_id))

        return data

    @classmethod
    def fetch_by(cls, **kwargs):
        return cls.model.fetch_by(**kwargs)
