import geocoder

from src.UoW.base_sevice import BaseUseCase
from src.UoW.utils.transaction import async_transactional
from src.modules.address.domain.model import Address
from src.modules.address.infrastructure.dto import AddressDtoOut, AddressDTOCommand, SearchAddressDto
from src.modules.address.infrastructure.uow import AddressUnitOfWork


class GeAddressUserUseCase(BaseUseCase[AddressUnitOfWork]):
    def __init__(self, uow: AddressUnitOfWork) -> None:
        self._uow = uow

    @async_transactional()
    async def invoke(self, data: SearchAddressDto) -> AddressDtoOut:
        address = await self.uow.repository.find_by_col(address=data.address)
        if not address:
            geo = geocoder.google('Mountain View, CA')
            address = Address.new_address(
                AddressDTOCommand(address=data.address, latitude=geo.latlng[0], longitude=geo.latlng[1]))
            self.uow.repository.create(address)

        return AddressDtoOut.model_validate(address.__dict__)
