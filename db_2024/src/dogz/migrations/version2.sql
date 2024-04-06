-- up

alter table person_dogs add constraint person_dogs_person__fk foreign key (person_id) references persons(id) on delete cascade;

alter table person_dogs add constraint person_dogs_dog__fk foreign key (dog_id) references dogs(id) on delete cascade;

-- down

alter table person_dogs drop constraint person_dogs_person__fk;

alter table person_dogs drop constraint person_dogs_dog__fk;


