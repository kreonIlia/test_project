from dataclasses import dataclass
from uuid import UUID, uuid4

from src.modules.address.infrastructure.dto import AddressDTOCommand


@dataclass
class Address:
    id: UUID
    address: str
    latitude: float
    longitude: float

    @staticmethod
    def new_address(command: AddressDTOCommand) -> 'Address':
        return Address(id=uuid4(), **command.model_dump())
