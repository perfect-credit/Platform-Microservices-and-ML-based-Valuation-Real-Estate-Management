from pymongo.errors import DuplicateKeyError

from models import Account


async def read_accout_by_phone_number(phone_number: str) -> Account:
    account = await Account.find(Account.phone_number == phone_number).first_or_none()
    return account


async def create_account(phone_number: str, name: str) -> Account:
    try:
        account = Account(phone_number=phone_number, name=name)
        await account.insert()
        return account
    except DuplicateKeyError:
        raise ValueError("Phone number already exists")
