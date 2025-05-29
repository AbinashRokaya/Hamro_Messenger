from sqlalchemy.orm import Session
from schemas.register_schema import User
from model.user_model import UserModel
from fastapi import APIRouter,Depends
from database.database import get_db
from auth.hasing import get_password_hased

route=APIRouter(
    prefix="/Register",
    tags=["Authenticate"]
)

@route.post("/")
def register(user:User,db:Session=Depends(get_db)):
    hashed_password=get_password_hased(user.password)
    new_user=UserModel(username=user.username,
                       email=user.email,
                       address=user.address,
                       age=user.age,
                       phone_number=user.phone_number,
                       password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"New user is added"}
    