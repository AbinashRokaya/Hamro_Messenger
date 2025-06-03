from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from database.database import get_db
from model.friends_model import FriendModel
from model.message_model import MessageModel
from model.user_model import UserModel
from auth.current_user import get_current_user
from schemas.token_schema import AuthenticateUser
from sqlalchemy.orm import Session
from schemas.messang_schema import MessageBase,MessageMedia,MessageWithoutMedia
from uuid import UUID
from database import database
from typing import Annotated
from model.media_model import MediaModel
from sqlalchemy import and_,or_


route=APIRouter(
    prefix="/message",
    tags=["Message"]
)

@route.post("/{user_id}")
def send_message(
    user_id: UUID,
    message_value: MessageBase,
   
    current_user: AuthenticateUser = Depends(get_current_user)
):
    with get_db() as db:
        return create_message(
            db=db,
            sender_id=current_user.user_id,
            receiver_id=user_id,
            message_text=message_value.message
        )



@route.get("/get_all_message/{user_id}")
def get_all_messages(user_id: UUID, current_user: AuthenticateUser = Depends(get_current_user)):
    with get_db() as db:
        all_messages = db.query(MessageModel).filter(
            or_(
                and_(
                    MessageModel.sender_id == current_user.user_id,
                    MessageModel.reciver_id == user_id
                ),
                and_(
                    MessageModel.sender_id == user_id,
                    MessageModel.reciver_id == current_user.user_id
                )
            )
        ).all()

        if not all_messages:
            raise HTTPException(status_code=404, detail="Not friend")

        all_message_list = []

        for message in all_messages:
            media = db.query(MediaModel).filter(MediaModel.message_id == message.message_id).first()

            if media:
                me = MessageMedia(
                    message_id=message.message_id,
                    sender_id=message.sender_id,
                    reciver_id=message.reciver_id,
                    file_url=media.file_url
                )
            else:
                me = MessageWithoutMedia(
                    message_id=message.message_id,
                    sender_id=message.sender_id,
                    reciver_id=message.reciver_id,
                    message=message.message
                )

            all_message_list.append(me)  # ✅ This should happen regardless of media

        return all_message_list


async def send_message_from_sender(
    sender_id: UUID,  # the authenticated user
    receiver_id: UUID,
    message_text: str
):
    with get_db() as db:
        message = MessageModel(
        sender_id=sender_id,
        reciver_id=receiver_id,
        message=message_text
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {"message is sent"}


def create_message(
    db: Session,
    sender_id: UUID,
    receiver_id: UUID,
    message_text: str
):
    friend_checking = db.query(FriendModel).filter(
        FriendModel.user_id_2 == receiver_id,
        FriendModel.friend_status == "accepted"
    ).first()

    if not friend_checking:
        raise HTTPException(status_code=404, detail="Not friend")

    message = MessageModel(
        sender_id=sender_id,
        reciver_id=receiver_id,
        message=message_text
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message
