from uuid import UUID

from src.adapters.dto.base import BaseRequestDTO


class AddressDTO(BaseRequestDTO):
    address: str
    latitude: float
    longitude: float


class AddressDTOCommand(AddressDTO):
    ...


class SearchAddressDto(BaseRequestDTO):
    address: str


class AddressDtoOut(AddressDTO):
    id: UUID
