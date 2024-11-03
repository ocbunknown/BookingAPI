from typing import Callable

from src.database.gateway import DBGateway

from .gateway import ServiceGateway

ServiceGatewayFactory = Callable[[], ServiceGateway]


def create_service_gateway_factory(
    database: Callable[[], DBGateway],
) -> ServiceGatewayFactory:
    def _create_instance() -> ServiceGateway:
        return ServiceGateway(database())

    return _create_instance


__all__ = (
    "ServiceGateway",
    "service_gateway_factory",
)
