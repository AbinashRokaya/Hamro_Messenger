from datetime import datetime
from auth.jwt import SECRET_KEY,ALGORITHM
from database.database import get_db
from fastapi import Depends,HTTPException,status
import jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from model.user_model import UserModel
from schemas.token_schema import TokenPayload,AuthenticateUser
from sqlalchemy.orm import Session

oauth2_schema=OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(get_db))->AuthenticateUser:

    try:
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
        token_data=TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp)<datetime.utcnow():
            raise HTTPException(
                status_code=401,detail="Token expired",
                heaters={"WWW-Authenticate":"Bearer"}
            )
        
    except(jwt.PyJWTError,ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentails",
            heaters={"WWW-Authenticate":"Bearer"}

        )
    authenticate_user=db.query(UserModel).filter(UserModel.email==token_data.sub).first()
    if not authenticate_user :
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    Users=AuthenticateUser(
        user_id=authenticate_user.user_id,
        email=authenticate_user.email,
        username=authenticate_user.username,
        phone_number=authenticate_user.phone_number,
        address=authenticate_user.address,
        age=authenticate_user.age
    )

    return Users

