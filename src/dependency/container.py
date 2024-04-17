from dependency_injector import providers
from dependency_injector.containers import copy

from src.core.containers import BaseContainer
from src.modules.address.infrastructure.uow import AddressUnitOfWork
from src.modules.address.usecase.get_address.service import GeAddressUserUseCase


@copy(BaseContainer)
class Container(BaseContainer):
    # Address
    address_uow = providers.Factory(AddressUnitOfWork, engine=BaseContainer.db.provided.engine)
    get_address_use_case = providers.Factory(GeAddressUserUseCase, uow=address_uow)
