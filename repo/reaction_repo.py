from database.database import get_db
from uuid import UUID
from schemas.reaction_schemas import ReactionSchemas
from model.user_model import UserModel
from model.friends_model import FriendModel
from model.reaction_model import ReactionModel
from fastapi import HTTPException,status

def send_reaction_all(message_id:UUID,current_user:UUID,reaction:ReactionSchemas):
    with get_db() as db:
        reaction=db.query(ReactionModel).filter(ReactionModel.message_id==message_id).first()

        if not reaction:
            raise HTTPException(status_code=404,detail={"Not found"})
        
        new_reaction=ReactionModel(
            message_id=message_id,
            user_id=current_user,
            reaction_type=reaction.reaction_type
        )

        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)
        return {"new reaction is added"}
    