from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from database.database import Base
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from model.message_model import MessageModel

class MediaModel(Base):
    __tablename__="media"

    media_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    message_id=Column(UUID(as_uuid=True),ForeignKey("message.message_id"))

    file_url=Column(String,nullable=False)
    file_type = Column(String(50), nullable=False)
    upload_timestamp = Column(DateTime, server_default=func.now())


