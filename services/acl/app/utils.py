from datetime import datetime, timezone


def validate_otp(otp: int) -> bool:
    timestamp = datetime.now(timezone.utc)
    valid_otp = f"{str(timestamp.day).zfill(2)}{str(timestamp.hour).zfill(2)}{str(timestamp.minute).zfill(2)}"
    return str(otp) == valid_otp
