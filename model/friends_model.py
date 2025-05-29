from database.database import Base
from sqlalchemy import String,Integer,Column,Enum,ForeignKey,DateTime
from schemas.status_schema import Friend_Status
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import UUID
from uuid import uuid4


class FriendModel(Base):
    __tablename__="friend"

    friend_id=Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id_1=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    user_id_2=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    friend_status=Column(Enum(Friend_Status),default=Friend_Status.pending)
    friendship_time=Column(DateTime,server_default=func.now())


    
