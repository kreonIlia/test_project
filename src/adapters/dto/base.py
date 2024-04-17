import uuid

from pydantic import BaseModel, ConfigDict


class BaseRequestDTO(BaseModel):
    """Base DTO Schema for Request"""

    pass


class BaseResponseDTO(BaseModel):
    """Base DTO Schema for Response"""

    model_config: ConfigDict = ConfigDict(
        from_attributes=True, populate_by_name=True
    )


class ResponseMsgDTO(BaseResponseDTO):
    """Message DTO Schema for Response"""

    message: str


class ResponseIdDTO(BaseResponseDTO):
    """Id DTO Schema for Response"""

    id: uuid.UUID
