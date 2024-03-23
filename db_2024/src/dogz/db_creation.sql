/*
AI

Create a table on postgres 15 database that would correspond to the following pydantic class

class Dog(BaseModel):
    id: UUID | None
    breed_id: UUID
    lineage: str
    birthdate: date
    name: str

For `str` fields use `text` type.
The `id` field should be generated per default.

*/

CREATE TABLE dogs (
    id UUID DEFAULT gen_random_uuid(),
    breed_id UUID NOT NULL,
    lineage TEXT NOT NULL,
    birthdate DATE NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE person (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    pesel TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT
);

create table person_dogs(
    dog_id UUID not null,
    person_id uuid not null,
    PRIMARY KEY (dog_id, person_id)
);
