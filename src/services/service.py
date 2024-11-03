from typing import Any, Generic, TypeVar

RepositoryType = TypeVar("RepositoryType")


class Service(Generic[RepositoryType]):
    def __init__(self, repository: RepositoryType, **kwargs: Any) -> None:
        self.repository = repository
        self.kwargs = kwargs
