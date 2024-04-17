from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.base_repository import AsyncRepository
from src.modules.address.domain.model import Address


class AddressRepository(AsyncRepository[Address, UUID]):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    ...
