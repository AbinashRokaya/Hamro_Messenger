from enum import Enum

class Friend_Status(str,Enum):
    pending="pending"
    accepted="accepted"
    blocked="blocked"