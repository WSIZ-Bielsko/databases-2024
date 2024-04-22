from uuid import UUID
from pydantic import BaseModel


class Kudo(BaseModel):
    id: UUID
    purpose: str  # id_przedmiotu lub inny
    owner_id: str  # album w WD
