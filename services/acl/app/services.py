from auth import create_token, decode_token
from pb.auth_pb2 import NoTokenResponse, TokenResponse, ValidateResponse
from pb.auth_pb2_grpc import AuthServiceServicer
from repositories import create_account, read_accout_by_phone_number
from utils import validate_otp


class AuthService(AuthServiceServicer):
    async def SendOtp(self, request, context) -> NoTokenResponse:
        try:
            await read_accout_by_phone_number(request.phone_number)
            return NoTokenResponse(success=True, message="Verify OTP")
        except ValueError:
            return NoTokenResponse(success=False, message="Phone number already exists")

    async def Register(self, request, context) -> TokenResponse:
        try:
            if validate_otp(request.otp):
                account = await create_account(request.phone_number, request.name)
                token = create_token(account)
                return TokenResponse(success=True, message="Account created", token=token)
            else:
                print(f"Invalid OTP: {request.otp}")
                raise ValueError("Invalid OTP")
        except ValueError as e:
            return TokenResponse(success=False, message=e.args[0], token="")

    async def Login(self, request, context) -> TokenResponse:
        try:
            account = await read_accout_by_phone_number(request.phone_number)
            if not account:
                raise ValueError("Phone number does not exist")

            if not validate_otp(request.otp):
                print(f"Invalid OTP: {request.otp}")
                raise ValueError("Invalid OTP")

            token = create_token(account)
            return TokenResponse(success=True, message="Logged in", token=token)
        except ValueError as e:
            return TokenResponse(success=False, message=e.args[0], token="")

    async def Validate(self, request, context) -> ValidateResponse:
        try:
            payload = decode_token(request.token)
            return ValidateResponse(permissions=[payload.get("sub")])
        except Exception:
            return ValidateResponse(permissions=[])
