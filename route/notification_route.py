from model.notifaction_model import NotificationModel
from sqlalchemy.orm import Session
from auth.current_user import get_current_user
from schemas.token_schema import AuthenticateUser
from fastapi import APIRouter,Depends,HTTPException,status
from database.database import get_db
from uuid import UUID

route=APIRouter(
    prefix="/Notification",
    tags=["Notification"]
)

@route.get("/all")
def get_all_notification(current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:
        notifaction_list=db.query(NotificationModel).filter(NotificationModel.user_id==current_user.user_id).all()
        if not notifaction_list:
            raise HTTPException(status_code=404,detail="Not found Notification")
        
        return notifaction_list


@route.post("/{notifaction_id}")
def notification_is_shown(notifaction_id:UUID,current_user:AuthenticateUser=Depends(get_current_user)):
    with get_db() as db:
        notification_check=db.query(NotificationModel).filter(NotificationModel.notification_id==notifaction_id).first()
        if not notification_check:
            raise HTTPException(status_code=404,detail="Notification not found")
        
        notification_check.is_read=True
        db.commit()
        db.refresh(notification_check)

        return notification_check.message