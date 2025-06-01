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
from repo import friend_repo
from sqlalchemy.sql import text
from sqlalchemy import and_,or_

from model.user_model import UserModel
from uuid  import UUID

route=APIRouter(
    prefix="/friend",
    tags=["Friend"]
)

@route.post("/")
def send_friend_request(friend:Friend,current_user:AuthenticateUser=Depends(get_current_user)):
    return friend_repo.send_friend_request(friend=friend,current_user=current_user)
        
       

        # return {f"friend request is sent to {friend_username.email}"}

    
@route.get("/")
def get_friend_request(current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:
        friend_request_message=db.query(NotificationModel).filter(NotificationModel.user_id==current_user.user_id).all()
        return friend_request_message


@route.get("/frend_request/all")
def friend_request_status(current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:
    
        friend_request=db.query(FriendModel).filter(FriendModel.user_id_2==current_user.user_id,
                                                FriendModel.friend_status=="pending" ).all()
        
        if not friend_request:
            raise HTTPException(status_code=404,detail="Not found friend request")
        return friend_request

@route.post("/friest_request_status/{friend_id}")
def friend_request_status(friend_id:UUID,frient_status:FriendRequest,current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:
        friend=db.query(UserModel).filter(UserModel.user_id==friend_id).first()

        if not friend:
            raise HTTPException(status_code=404,detail="Not found")
        
        friend_request=db.query(FriendModel).filter(FriendModel.user_id_2==current_user.user_id,
                                                    FriendModel.user_id_1==friend.user_id).first()
        # get_friend_status=frient_status.Friend_Status
        print(f"{frient_status.Friend_Status} ")
        friend_request.friend_status=frient_status.Friend_Status
        print(friend_request)

        db.commit()
        db.refresh(friend_request)


        
        return {"user_id":friend_request.user_id_1}

@route.post("/search_friend/{friend_name}")
def search_friend(friend_name:str,current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:
        friend_list=db.query(UserModel).filter(UserModel.username.like(f"%{friend_name}%")).all()

        if not friend_list:
            raise HTTPException(status_code=404,detail=f"{friend_name} not found")
        
        return friend_list

@route.get("/all_friend")
def get_all_friend(current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:

        accepted_friends = db.query(FriendModel).filter(
                and_(
                    FriendModel.friend_status == 'accepted',
                    or_(
                        FriendModel.user_id_1 == current_user.user_id,
                        FriendModel.user_id_2 == current_user.user_id
                    )
                )
            ).all()
        if not accepted_friends:
            raise HTTPException(status_code=404,detail=f"friend not found")
        
        friend_list=[]
        for friend_id in accepted_friends:
            if friend_id.user_id_1 == current_user.user_id:
                friend_list.append(friend_id.user_id_2)
            elif friend_id.user_id_2== current_user.user_id:
                friend_list.append(friend_id.user_id_1)
        friend_detail=[]
        for id in friend_list:
            fr=db.query(UserModel).filter(UserModel.user_id==id).first()
            friend_detail.append(fr)

        
        return friend_detail