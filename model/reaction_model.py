from sqlalchemy import Column,String,Integer,Boolean,DateTime,Enum,ForeignKey
from schemas.status_schema import ReactionType
from sqlalchemy.sql import func
from uuid import uuid4
from sqlalchemy.types import UUID
from database.database import Base


class ReactionModel(Base):
    __tablename__="reaction"

    message_reaction_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    message_id=Column(UUID(as_uuid=True),ForeignKey("message.message_id"))
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    reaction_type=Column(Enum(ReactionType))
    created_time=Column(DateTime,server_default=func.now())