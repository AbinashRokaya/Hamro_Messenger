from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID
from uuid import uuid4

class UserModel(Base):
    __tablename__="user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    address=Column(String)
    age=Column(Integer)
    phone_number=Column(String)
    password=Column(String)
    created_at=Column(DateTime,server_default=func.now())
    updated_at=Column(DateTime,server_default=func.now())

   
    