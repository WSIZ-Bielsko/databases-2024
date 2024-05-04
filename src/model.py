from datetime import time

from pydantic import BaseModel, field_serializer


class Lecture(BaseModel):
    przedmiotid: int
    nazwa: str
    active: bool


class Teacher(BaseModel):
    wykladowcaid: int
    # sid: str | int | None
    imie: str
    nazwisko: str
    prefix: str
    suffix: str | None
    active: bool


class Group(BaseModel):
    grupaid: int  # to jest "ID", odpowiada temu kolumna primary key
    nazwa: str
    opis: str
    active: bool


class PlanItem(BaseModel):
    id: int | None
    group_id: int
    lecture_id: int
    teacher_id: int
    room: str
    hour: time
    day_of_week: str

    @field_serializer("hour")
    def serialize_time(self, d: time, _info):
        return str(d)


if __name__ == "__main__":
    g = Group(grupaid=1, nazwa="G", opis="gg", active=True)
    print(g.dict())
