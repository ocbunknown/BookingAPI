from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models import Base
from src.database.models.base.mixins import ModelWithIDMixin


class User(ModelWithIDMixin, Base):
    phone: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    email: Mapped[Optional[str]] = mapped_column(String, index=True, unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
