from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.dependency.container import Container
from src.modules.address.infrastructure.dto import AddressDtoOut, SearchAddressDto
from src.modules.address.usecase import router
from src.modules.address.usecase.get_address.service import GeAddressUserUseCase


@router.post("",
             name="Get address",
             summary="Получение адреса",
             response_model=AddressDtoOut,
             )
@inject
async def get_address(data: SearchAddressDto,
                      uc: GeAddressUserUseCase = Depends(Provide[Container.get_address_use_case]),
                      ):
    model = await uc.invoke(data)
    return model
