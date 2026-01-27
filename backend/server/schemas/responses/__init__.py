from pydantic import Field

from server.schemas import BaseResponseSchema


class CountResponse(BaseResponseSchema):
    count: int = Field(0, description="Number of items")


class StatusResponse(BaseResponseSchema):
    success: bool = Field(..., description="Status of the request")
    message: str | None = Field(None, description="Message from the server")
