from pydantic import BaseModel,EmailStr
from schemas.status_schema import Friend_Status
from uuid import UUID

class Friend(BaseModel):
    username:str

class FriendRequest(BaseModel):
    
    Friend_Status:Friend_Status


class FriendAccepted(BaseModel):
    friend_id:UUID