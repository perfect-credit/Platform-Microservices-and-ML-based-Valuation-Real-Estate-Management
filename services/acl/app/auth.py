from datetime import datetime, timedelta, timezone

import jwt

from config import settings
from models import Account


def create_token(account: Account) -> str:
    payload = {
        "sub": str(account.phone_number),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE),
    }
    return jwt.encode(payload, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.exceptions.InvalidTokenError as e:
        raise e
