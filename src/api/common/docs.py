from pydantic import BaseModel


class BaseDoc(BaseModel):
    message: str


class UnAuthorizedError(BaseDoc):
    pass


class NotFoundError(BaseDoc):
    pass


class BadRequestError(BaseDoc):
    pass


class TooManyRequestsError(BaseDoc):
    pass


class ServiceUnavailableError(BaseDoc):
    pass


class ForbiddenError(BaseDoc):
    pass


class ServiceNotImplementedError(BaseDoc):
    pass


class ConflictError(BaseDoc):
    pass
