from typing import Protocol


class AbstractHasher(Protocol):
    def hash_password(self, plain: str) -> str: ...

    def verify_password(self, hashed: str, plain: str) -> bool: ...
