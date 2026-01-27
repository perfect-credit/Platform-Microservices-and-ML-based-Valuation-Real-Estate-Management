from datetime import datetime, timezone
from typing import Annotated

import pymongo
from beanie import Document, Indexed
from pydantic import Field


class BaseDocument(Document):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date and time of the document creation",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date and time of the document update",
    )

    class Settings:
        use_cache = True
        use_revision = True
        use_state_management = True
        validation_on_save = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Settings.name = f"{cls.__name__.lower()}s"


class Account(BaseDocument):
    phone_number: Annotated[str, Indexed(unique=True)] = Field(
        ...,
        description="Unique phone number of the account",
        max_length=20,
    )
    name: Annotated[str, Indexed(index_type=pymongo.TEXT)] = Field(
        ...,
        description="The name of the account",
        max_length=64,
    )
