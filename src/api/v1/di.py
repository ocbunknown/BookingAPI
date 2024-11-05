from typing import Callable, TypeVar

from fastapi import FastAPI

from src.api.v1.handlers import MediatorImpl, setup_mediator
from src.common.interfaces.mediator import MediatorProtocol
from src.common.security.argon2 import get_argon2_hasher
from src.core.settings import Settings
from src.database import create_database_factory
from src.database.core.connection import create_sa_engine, create_sa_session_factory
from src.database.core.manager import TransactionManager
from src.services import create_service_gateway_factory

DependencyType = TypeVar("DependencyType")


def singleton(dependency: DependencyType) -> Callable[[], DependencyType]:
    def singleton_factory() -> DependencyType:
        return dependency

    return singleton_factory


def setup_dependencies(app: FastAPI, settings: Settings) -> None:
    engine = create_sa_engine(
        settings.db.url,
        pool_size=settings.db.connection_pool_size,
        max_overflow=settings.db.connection_max_overflow,
        pool_pre_ping=settings.db.connection_pool_pre_ping,
    )

    session_factory = create_sa_session_factory(engine)
    database_factory = create_database_factory(TransactionManager, session_factory)
    service_factory = create_service_gateway_factory(database_factory)
    hasher = get_argon2_hasher()

    app.state.engine = engine

    mediator = MediatorImpl()
    setup_mediator(
        mediator,
        gateway=service_factory,
        hasher=hasher,
    )

    app.dependency_overrides[MediatorProtocol] = singleton(mediator)
