from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, field_serializer


class Dog(BaseModel):
    id: UUID | None
    breed_id: UUID
    lineage: str
    birthdate: date
    name: str

    # serializers written per hand

    @field_serializer('id')
    def serialize_id(self, id: UUID, _info):
        return str(id)

    @field_serializer('breed_id')
    def serialize_breed_id(self, breed_id: UUID, _info):
        return str(breed_id)

    @field_serializer('birthdate')
    def serialize_birthdate(self, birthdate: date, _info):
        return str(birthdate)


class Person(BaseModel):
    id: UUID | None
    pesel: str
    name: str
    phone: str
    password_hash: str


class Surgery(BaseModel):
    id: UUID | None
    dog_id: UUID
    date_performed: datetime
    description: str


class AccessLevel(BaseModel):
    level: str
    # [client, doctor, admin]



"""
Generate postgres 15 table for the following pydantic dataclass

class Person(BaseModel):
    id: UUID | None
    pesel: str
    name: str
    phone: str

The id field should be random-generated per default, str should be represented as text;

"""
