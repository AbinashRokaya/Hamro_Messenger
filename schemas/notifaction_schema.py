from pydantic import BaseModel
from uuid import UUID

class notifactionBase(BaseModel):
    user_id:UUID
    message:str


class NotifactionCreateRequest(notifactionBase):
    pass