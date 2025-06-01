from database.database import get_db
from fastapi import APIRouter,Depends,HTTPException,status
from schemas.friends_schema import Friend,FriendRequest
from model.notifaction_model import NotificationModel
from model.user_model import UserModel
from model.friends_model import FriendModel
from sqlalchemy.orm import Session
from auth.current_user import get_current_user
from schemas.token_schema import AuthenticateUser
from schemas.notifaction_schema import NotifactionCreateRequest
from model.notifaction_model import NotificationModel

from model.user_model import UserModel
from uuid  import UUID


def send_friend_request(friend:Friend,current_user:AuthenticateUser):
    with get_db() as db:
       

        friend_username=db.query(UserModel).filter(UserModel.username==friend.username).first()

        check_if_friend=db.query(FriendModel).filter(FriendModel.user_id_2==friend_username.user_id).first()

        if check_if_friend:
            raise HTTPException(status_code=409,detail=f"{friend_username.username} is already friend")

        if not friend_username:
            raise HTTPException(status_code=404,detail=f"Friend email {friend.username} is not found")
        

        new_friend=FriendModel(user_id_1=current_user.user_id,
                            user_id_2=friend_username.user_id,
                            )
        
        mssage_response=f"{current_user.username} has send a friend request"

        new_message=NotificationModel(
            user_id=friend_username.user_id,
            message=mssage_response
        )

        db.add_all([new_friend,new_message])
        
        db.add(new_friend)
        db.commit()
        db.refresh(new_friend)
        db.refresh(new_message)

        return {"user_id":new_friend.friend_id}
