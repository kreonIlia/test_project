import geocoder

from src.UoW.base_sevice import BaseUseCase
from src.UoW.utils.transaction import async_transactional
from src.modules.address.domain.model import Address
from src.modules.address.infrastructure.dto import AddressDtoOut, AddressDTOCommand, SearchAddressDto
from src.modules.address.infrastructure.uow import AddressUnitOfWork
from fastapi import HTTPException


class GeAddressUserUseCase(BaseUseCase[AddressUnitOfWork]):
    def __init__(self, uow: AddressUnitOfWork) -> None:
        self._uow = uow

    @async_transactional()
    async def invoke(self, data: SearchAddressDto) -> AddressDtoOut:
        address = await self.uow.repository.find_by_col(address=data.address)

        if not address:
            geo_data = geocoder.arcgis(data.address)

            if not geo_data.ok:
                raise HTTPException(status_code=404, detail="Адрес не обнаружен")

            address = Address.new_address(
                AddressDTOCommand(
                    address=data.address,
                    latitude=geo_data.json['lat'],
                    longitude=geo_data.json['lng']
                )
            )
            self.uow.repository.create(address)

        return AddressDtoOut.model_validate(address.__dict__)
