from http import HTTPStatus
from .base_exception import ApiException


class ValidationException(ApiException):
    """Custom ValidationError Exception Class"""

    def __init__(self, message="Bucket with the same name already exists. Please try creating with another name.", data=None):
        super(ValidationException, self).__init__(message, data)
        self.status_code = HTTPStatus.FORBIDDEN
