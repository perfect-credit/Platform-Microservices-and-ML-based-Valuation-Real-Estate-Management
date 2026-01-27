from pydantic import Field

from server.schemas import BaseResponseSchema


class Ad(BaseResponseSchema):
    id: str = Field(..., description="ID of the ad")
    title: str = Field(..., description="Title for the ad")
    description: str = Field(..., description="Description of the property of the ad")
    property_id_nma: str = Field(..., description="Property ID of the ad")
    address: str = Field(..., description="Address of the property of the ad")
    price: float = Field(..., description="Expecte price of the property of the ad")
    type: str = Field(..., description="Type of the ad")
    status: str = Field(..., description="Status of the ad")
    listed_by: str = Field(..., description="Name of the person who listed the ad")
