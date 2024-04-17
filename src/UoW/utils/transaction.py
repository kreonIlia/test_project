from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.ext.asyncio import AsyncSession


async def __async_requires_new(self, func, read_only: bool, session: AsyncSession, args, kwargs):
    if not session.is_active:
        await session.begin()

    result = await func(self, *args, **kwargs)
    if not read_only:
        await session.commit()
        try:
            inspect(result)
            await session.refresh(result)
        except NoInspectionAvailable:
            pass

    return result


def async_transactional(read_only: bool = False):
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            if hasattr(self, 'uow'):
                async with self.uow:
                    result = await __async_requires_new(self=self, func=func, read_only=read_only,
                                                        session=self.uow.session, args=args, kwargs=kwargs)

                    return result

        return wrapper

    return decorator
