from typing import Optional
from pydantic import BaseModel, validator
import re


class User(BaseModel):
    id: Optional[str]
    username: str
    password: str

    @validator("username")
    def val_username(cls, p):
        if not p or len(p) < 1:
            raise ValueError("username must be provided")
        if 8 > len(p):
            raise ValueError("username must contain at least 8 characters")
        if len(p) > 30:
            raise ValueError("username must be less than 30 characters")
        return p

    @validator("password")
    def val_password(cls, p):
        if not (8 < len(p) < 17):
            raise ValueError("Password must be (8-16) characters long")
        if re.match(
            r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$!?¿&*%])[\w\d@#$!?¿&*%]{8,12}$",
            p,
        ):
            return p
        else:
            raise ValueError(
                "Password must contain at least: an upper case, a lower case, a number, a special character[@#$!?¿&*%]"
            )
