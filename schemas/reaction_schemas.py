from pydantic import BaseModel
from schemas.status_schema import ReactionType
from uuid import UUID


class ReactionSchemas(BaseModel):
    reaction_type:ReactionType
  