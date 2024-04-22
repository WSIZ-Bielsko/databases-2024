
create table plan(
    id serial primary key,
    group_id int,
    lecture_id int,
    teacher_id int,
    room text,
    hour time,
    day_of_week text
);

create table groups(
    grupaid serial primary key,
    nazwa text,
    opis text,
    active bool
);

create table lectures(
    przedmiotid serial primary key,
    nazwa text,
    active bool
);

create table teachers(
    wykladowcaid serial primary key,
    imie text,
    nazwisko text,
    prefix text,
    suffix text,
    active bool
);
