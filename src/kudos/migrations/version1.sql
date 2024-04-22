
create table Kudo
(
    id       UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    purpose  TEXT,
    owner_id TEXT NOT NULL
);


-- down

drop table if exists Kudo;

