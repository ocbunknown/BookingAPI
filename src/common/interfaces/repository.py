from typing import Any, Protocol, Type


class Repository(Protocol):
    """A protocol representing a Repository pattern.

    A Repository mediates between the domain and data mapping layers, acting like
    an in-memory domain object collection. It provides a way to query and
    manipulate the data without needing to know about the underlying data source
    or ORM specifics.

    Attributes
    ----------
        model (Type[Any]): A class reference indicating the type of model
                           the repository will be handling. This could be a
                           database model or any other type of data structure.

    """

    model: Type[Any]
