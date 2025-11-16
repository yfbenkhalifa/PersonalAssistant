from attr import dataclass


@dataclass 
class Message: 
    value: str
    owner: str