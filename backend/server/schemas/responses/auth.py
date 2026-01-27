from pydantic import Field

from server.schemas import BaseResponseSchema


class AuthResponse(BaseResponseSchema):
    access_token: str = Field(..., description="Access token")
    token_type: str = Field(..., description="Token type")
