from typing import Any, Dict, Optional


class AppException(Exception):
    def __init__(
        self,
        message: str = "App exception",
        status_code: int = 500,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.content = {"message": message}
        self.headers = headers
        self.status_code = status_code

    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__


class DetailedError(AppException):
    status_code: int = 500

    def __init__(
        self,
        message: str,
        headers: Optional[Dict[str, Any]] = None,
        **additional: Any,
    ) -> None:
        super().__init__(
            message=message,
            status_code=self.status_code,
            headers=headers,
        )
        self.content |= additional

    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.content}\nHeaders: {self.headers or ''}"


class UnAuthorizedError(DetailedError):
    status_code: int = 401


class NotFoundError(DetailedError):
    status_code: int = 404


class BadRequestError(DetailedError):
    status_code: int = 400


class TooManyRequestsError(DetailedError):
    status_code: int = 429


class ServiceUnavailableError(DetailedError):
    status_code: int = 503


class ForbiddenError(DetailedError):
    status_code: int = 403


class ServiceNotImplementedError(DetailedError):
    status_code: int = 501


class ConflictError(DetailedError):
    status_code: int = 409
