from http import HTTPStatus
from .base_exception import ApiException


class BucketAlreadyCreatedException(ApiException):
    """Custom bucket already created exception class"""

    def __init__(self, message='Your previous request to create the named bucket succeeded and you already own it.', data=None):
        super(BucketAlreadyCreatedException, self).__init__(message, data)
        self.status_code = HTTPStatus.CONFLICT


class BucketAlreadyExistsException(ApiException):
    """Custom bucket already exists Exception Class"""

    def __init__(self, message="Bucket with the same name already exists. Please try creating with another name.", data=None):
        super(BucketAlreadyExistsException, self).__init__(message, data)
        self.status_code = HTTPStatus.BAD_REQUEST


class BucketDoesNotExistException(ApiException):
    """Custom bucket does not exist exception"""

    def __init__(self, message="The specified bucket does not exist.", data=None):
        super(BucketDoesNotExistException, self).__init__(message, data)
        self.status_code = HTTPStatus.BAD_REQUEST
