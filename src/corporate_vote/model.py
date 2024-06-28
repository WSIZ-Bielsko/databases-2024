from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    email: str
    password: str
    token: str
    shares: int
    active: bool
    is_admin: bool = False


# user logs in, new token created

class Results(BaseModel):
    yes_count: int
    no_count: int
    pass_count: int


class Participation(BaseModel):
    email: str
