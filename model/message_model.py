from database.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from sqlalchemy.sql import func
from sqlalchemy.types import UUID
from uuid import uuid4

class MessageModel(Base):
    __tablename__="message"

    message_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    sender_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    reciver_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    message=Column(String)
    created_at=Column(DateTime,server_default=func.now())