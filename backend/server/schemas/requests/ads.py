from pydantic import Field

from server.schemas import BaseRequestSchema


class CreateAdRequest(BaseRequestSchema):
    title: str = Field(..., description="Title of the ad")
    description: str = Field(..., description="Description of the ad")
    address: str = Field(..., description="Address of the property")
    property_id_nma: str = Field(..., description="Property ID NMA")
    price: float = Field(..., description="Price of the property")
    type: str = Field(..., description="Type of the property")


class UpdateAdRequest(BaseRequestSchema):
    title: str | None = Field(None, description="Title of the ad")
    description: str | None = Field(None, description="Description of the ad")
    address: str | None = Field(None, description="Address of the property")
    price: float | None = Field(None, description="Price of the property")
    type: str | None = Field(None, description="Type of the property")
    status: str | None = Field(None, description="Status of the property")
