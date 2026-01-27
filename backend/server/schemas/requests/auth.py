from pydantic import Field

from server.schemas import BaseRequestSchema


class LoginRequest(BaseRequestSchema):
    phone_number: str = Field(..., description="Phone number to login")
    otp: str = Field(..., description="OTP received on the phone number")


class RegisterRequest(LoginRequest):
    name: str = Field(..., description="Name of the user")
