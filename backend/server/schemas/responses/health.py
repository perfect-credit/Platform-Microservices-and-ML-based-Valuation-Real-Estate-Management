from datetime import datetime, timezone

from pydantic import Field

from server.schemas import BaseResponseSchema


class HealthResponse(BaseResponseSchema):
    APP_NAME: str = Field(description="The name of the application.")
    VERSION: str = Field(description="The version of the application.")
    TIME: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="The current time.")
