from src.UoW.async_alchemy_uow import AsyncAlchemyUnitOfWork
from sqlalchemy.ext.asyncio import AsyncEngine

from src.modules.address.infrastructure.repository import AddressRepository


class AddressUnitOfWork(AsyncAlchemyUnitOfWork):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine)

    async def __aenter__(self):
        await super().__aenter__()

        self.repository: AddressRepository = AddressRepository(self.session)
