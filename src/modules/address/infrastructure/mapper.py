from src.entity.db import mapper_registry
from src.entity.models import AddressEntity
from src.modules.address.domain.model import Address


def start_mapper():
    user_entity_tbl = AddressEntity.__table__

    mapper_registry.map_imperatively(
        Address,
        user_entity_tbl,
    )
