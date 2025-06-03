from pydantic import BaseModel
from uuid import UUID


class MediaBase(BaseModel):

    file_url:str
    


class MediaCreate(MediaBase):
    pass