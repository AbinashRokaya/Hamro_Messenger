from enum import Enum

class Friend_Status(str,Enum):
    pending="pending"
    accepted="accepted"
    blocked="blocked"


class ReactionType(str,Enum):
    like="like"
    love="love"
    laugh = "laugh"
    sad = "sad"
    angry = "angry"