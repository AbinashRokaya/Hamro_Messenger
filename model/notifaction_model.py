
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Boolean
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import UUID
from uuid import uuid4

class NotificationModel(Base):
    __tablename__="notifaction"

    notification_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    message=Column(String)
    is_read=Column(Boolean,default=False)
    created_at=Column(DateTime,server_default=func.now())