from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from server.dependencies.grpc import AuthClient


async def authenticate_user(
    client: Annotated[AuthClient, Depends(AuthClient)],
    authorization: Annotated[str, Header(alias="Authorization")],
) -> str:
    try:
        if not authorization:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No token found")
        res = client.validate(authorization)
        phone_number = res.get("permissions")[0]
        if "permissions" not in res:
            raise Exception("No permissions found")
        return phone_number
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
