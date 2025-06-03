from auth import current_user
from schemas.token_schema import AuthenticateUser
from fastapi import APIRouter,File,UploadFile,Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from auth.current_user import get_current_user
from uuid import UUID
from route.message_route import create_message
from database.database import get_db
from model.media_model import MediaModel
import os
import shutil
from pathlib import Path
from model.friends_model import FriendModel
from model.user_model import UserModel
from sqlalchemy import and_,or_

route=APIRouter(
    prefix="/media",
    tags=["Media"]
)
route.mount("/uploads",StaticFiles(directory="static/uploads"),name="uploads")

@route.post("/upload/{friend_id}")
async def upload_file(friend_id:UUID,file:UploadFile=File(...),current_user:AuthenticateUser=Depends(get_current_user)):

    with get_db() as db:
        accepted_friends = db.query(FriendModel).filter(
                and_(
                    FriendModel.friend_status == 'accepted',
                    or_(
                        FriendModel.user_id_1 == friend_id,
                        FriendModel.user_id_2 == friend_id
                    )
                )
            ).first()
        if not accepted_friends:
            raise HTTPException(status_code=404,detail="Not found")
        message=create_message(db=db,sender_id=current_user.user_id,receiver_id=friend_id,message_text="")
        file_ext = Path(file.filename).suffix.lower()

        if file_ext in [".png", ".jpg", ".jpeg", ".gif"]:
            save_path = f"static/uploads/images/{file.filename}"
            file_url = f"/uploads/images/{file.filename}"
        elif file_ext in [".mp4", ".avi", ".mov"]:
            save_path = f"static/uploads/videos/{file.filename}"
            file_url = f"/uploads/videos/{file.filename}"

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        os.makedirs(os.path.dirname(save_path),exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)


        new_media=MediaModel(
            message_id=message.message_id,
            file_url=file_url,
            file_type=file_ext,
        )

        db.add(new_media)
        db.commit()
        db.refresh(new_media)

        return new_media