import jwt
from jwt.exceptions import InvalidTokenError
import os 
from datetime import datetime,timedelta
from typing import Union,Any

SECRET_KEY="IcLnEKT4POz3fzkzikJ4bDiiyClSQB6iMNXtZRhvOoE"
ALGORITHM="HS256"
ACCESS_TOKEN_MINUTES=30

def create_access_token(subject:Union[str,Any],expires_delta:int=None)->str:
    if expires_delta:
        expires_delta=datetime.utcnow()+expires_delta
    else:
        expires_delta=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_MINUTES)

    to_encode={"exp":expires_delta,"sub":subject}
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_jwt