# instalacja:
```
poetry update  #możliwe, że niektóre biblioteki będą ~~ dziwnie sie instalowały na Państwa systemie operacyjnym
```
--> potencjalnie dostosować .env z loalizacją bazy danych

# działanie z alembic-iem

```
alembic init alembic
alembic revision -m 'create table users' 
alembic upgrade head
alembic downgrade -1
alembic current     # current version of DB
alembic history     # show a list of all migrations
```
