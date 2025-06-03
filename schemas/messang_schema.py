from pydantic import BaseModel
from uuid import UUID


class MessageBase(BaseModel):
    message:str
   

class MessageMedia(BaseModel):
    message_id:UUID
    sender_id:UUID
    reciver_id:UUID
    file_url:str

class MessageWithoutMedia(BaseModel):
   
    message_id:UUID
    sender_id:UUID
    reciver_id:UUID
    message:str