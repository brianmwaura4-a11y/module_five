from typing import Any


class AppException(Exception):
    def __init__(self, message: str = "Error", status_code: int = 500, payload: Any = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ConflictError(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation error", payload: Any = None):
        super().__init__(message, 400, payload)


class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, 401)


class AuthorizationError(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, 403)
