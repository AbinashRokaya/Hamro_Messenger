from pydantic import BaseModel,EmailStr
from typing import List,Optional
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):

    username:str
    email:EmailStr
    address:str
    age:int
    phone_number:PhoneNumber
    password:str

