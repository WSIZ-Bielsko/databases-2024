
-- up

ALTER TABLE persons
    ADD COLUMN password_hash TEXT;

CREATE TABLE surgeries
(
    id             UUID DEFAULT gen_random_uuid(),
    dog_id         UUID      NOT NULL,
    date_performed TIMESTAMP NOT NULL,
    description    TEXT      NOT NULL,
    PRIMARY KEY (id),
    foreign key (dog_id) references dogs (id) on delete cascade
);

create table Person2Surgery
(
    surgery_id UUID not null,
    person_id  UUID not null,
    PRIMARY KEY (surgery_id, person_id),
    foreign key (surgery_id) references surgeries (id) on delete cascade,
    foreign key (person_id) references persons (id) on delete cascade
);

CREATE TABLE AccessLevel
(
    level TEXT NOT NULL,
    PRIMARY KEY (level)
);

CREATE TABLE Person2Access
(
    person_id UUID NOT NULL,
    level     TEXT NOT NULL,
    PRIMARY KEY (person_id, level),
    foreign key (person_id) references persons (id) on delete cascade,
    foreign key (level) references accesslevel (level) on delete cascade
);

INSERT INTO AccessLevel (level) VALUES
                                      ('admin'),
                                      ('client'),
                                      ('doctor');

-- down

alter table persons
    drop column password_hash;

drop table person2access;
drop table person2surgery;
drop table surgeries;
drop table accesslevel;
