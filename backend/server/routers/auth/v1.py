from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from server.dependencies.auth import authenticate_user
from server.dependencies.grpc import AuthClient
from server.schemas.requests.auth import LoginRequest, RegisterRequest
from server.schemas.responses import StatusResponse
from server.schemas.responses.auth import AuthResponse


def router_factory() -> APIRouter:
    router = APIRouter(prefix="/v1/auth", tags=["Authentication System"])

    @router.get("/otp", response_model=StatusResponse)
    async def send_otp(
        phone_number: Annotated[str, Query(..., alias="phone-number", description="Phone number to send OTP to")],
        client: Annotated[AuthClient, Depends(AuthClient)],
    ):
        return client.send_otp(phone_number)

    @router.post("/register", response_model=AuthResponse)
    async def register(
        payload: Annotated[RegisterRequest, Body(..., description="Payload to register")],
        client: Annotated[AuthClient, Depends(AuthClient)],
    ):
        res = client.register(payload)
        return AuthResponse(access_token=res["token"], token_type="bearer")

    @router.post("/login", response_model=AuthResponse)
    async def login(
        payload: Annotated[LoginRequest, Body(..., description="Payload to login")],
        client: Annotated[AuthClient, Depends(AuthClient)],
    ):
        res = client.login(payload)
        return AuthResponse(access_token=res["token"], token_type="bearer")

    @router.get("/validate", dependencies=[Depends(authenticate_user)], response_model=StatusResponse)
    async def validate():
        return {"success": True, "message": "Validated"}

    return router
