from uuid import UUID
from pydantic import BaseModel, field_serializer


class Kudo(BaseModel):
    id: UUID
    purpose: str  # id_przedmiotu lub inny
    owner_id: str  # album w WD

    @field_serializer('id')
    def serialize_id(self, id: UUID, _info):
        return str(id)
