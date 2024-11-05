from uuid import UUID as uuid_type
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithUUIDMixin:
    """BaseUUID model class that represents ID with an UUID type"""

    uuid: Mapped[uuid_type] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
        index=True,
        nullable=False,
    )
