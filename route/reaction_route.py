from fastapi import APIRouter,Depends,HTTPException,status
from database.database import get_db
from model.user_model import UserModel
from model.friends_model import FriendModel
from model.reaction_model import ReactionModel
from uuid import UUID
from auth.current_user import get_current_user
from schemas.token_schema import AuthenticateUser
from repo import reaction_repo
from schemas.reaction_schemas import ReactionSchemas



route=APIRouter(
    prefix="/message_reaction",
    tags=['Message_reaction']
)


@route.post("/{message_id}")
def post_send_reaction(message_id:UUID,reaction_type:ReactionSchemas,current_user:AuthenticateUser=Depends(get_current_user)):
    return reaction_repo.send_reaction_all(message_id=message_id,current_user=current_user.user_id,reaction=reaction_type)