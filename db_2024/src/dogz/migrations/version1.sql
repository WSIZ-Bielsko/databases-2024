
-- up

CREATE TABLE dogs (
    id UUID DEFAULT gen_random_uuid(),
    breed_id UUID NOT NULL,
    lineage TEXT NOT NULL,
    birthdate DATE NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE persons (
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



-- down

drop table person_dogs;
drop table persons;
drop table dogs;