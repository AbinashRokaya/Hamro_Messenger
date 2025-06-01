from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token_schema import Token
from auth.hasing import verify_password
from database.database import get_db
from sqlalchemy.orm import Session
from auth.jwt import create_access_token
from model.user_model import UserModel


route=APIRouter(
    prefix=("/auth"),
    tags=['login']
)

@route.post("/login",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    with get_db() as db:
        get_user=db.query(UserModel).filter(UserModel.username==form_data.username).first()
        if not get_user:
            raise HTTPException(status_code=404,detail=f"User is not foud or email is Incorrect")
        
        if not verify_password(form_data.password,get_user.password):

            raise HTTPException(status_code=400,detail="Incorrect password")
        
        access_token=create_access_token(get_user.email)

        return {"access_token":access_token,"token_type":"bearer"}