from pydantic import BaseModel,EmailStr
from schemas.status_schema import Friend_Status

class Friend(BaseModel):
    username:str