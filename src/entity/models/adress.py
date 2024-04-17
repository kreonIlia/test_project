from src.entity.models.entity import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float


class AddressEntity(BaseEntity):
    __tablename__ = "addresses"

    address: Mapped[str] = mapped_column(String, unique=True, index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
