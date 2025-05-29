from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber 
from uuid import UUID

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenPayload(BaseModel):
    sub:str
    exp:int

class AuthenticateUser(BaseModel):
    user_id:UUID
    username:str
    email:EmailStr
    phone_number:PhoneNumber
    address:str
    age:int