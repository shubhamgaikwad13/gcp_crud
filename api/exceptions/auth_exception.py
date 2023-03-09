from http import HTTPStatus
from .base_exception import ApiException


class AuthException(ApiException):
    """Custom authentication Exception Class"""

    def __init__(self, message="Unauthorized Access", data=None):
        super(AuthException, self).__init__(message, data)
        self.status_code = HTTPStatus.UNAUTHORIZED


class NoTokenException(ApiException):
    """Custom token exception class"""
    def __init__(self, message="No authentication token provided.", data=None):
        super(NoTokenException, self).__init__(message, data)
        self.status_code = HTTPStatus.UNAUTHORIZED


class InvalidTokenException(ApiException):
    """Custom invalid token exception class"""

    def __init__(self, message="Invalid authentication token.", data=None):
        super(InvalidTokenException, self).__init__(message, data)
        self.status_code = HTTPStatus.UNAUTHORIZED
