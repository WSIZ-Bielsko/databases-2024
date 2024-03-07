import os
from asyncio import run

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from model import *

load_dotenv()  # take environment variables from .env.

DEFAULT_DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'

DATABASE_URL = os.getenv('DB_URL', DEFAULT_DATABASE_URL)


class DbService:

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        try:
            self.pool = await asyncpg.create_pool(self.database_url,
                                                  min_size=5, max_size=10,
                                                  timeout=30, command_timeout=5)
            logger.info('database connected!')
        except Exception as e:
            logger.error(f'Error connecting to DB, {e}')

    async def create_plan(self, item: PlanItem):
        logger.info('plan item creating')
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('''insert into plan(group_id,lecture_id,room,hour,day_of_week,teacher_id) 
                                               VALUES ($1, $2, $3, $4, $5, $6) returning *''',
                                            item.group_id, item.lecture_id, item.room,
                                            item.hour, item.day_of_week, item.teacher_id)
        created = PlanItem(**dict(row))
        logger.info(f'plan item created: {created}')

        return created  # with db-generated id

    async def update_plan(self, item: PlanItem) -> PlanItem:
        logger.info(f'plan item id={item.id} update: {item}')
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('''update plan set group_id=$2, lecture_id=$3, 
                                               room=$4, hour=$5, day_of_week=$6, teacher_id=$7 where id=$1 returning *''',
                                            item.id, item.group_id, item.lecture_id, item.room, item.hour,
                                            item.day_of_week, item.teacher_id)
        updated = PlanItem(**dict(row))
        logger.info(f'plan item updated: {updated}')
        return updated

    async def delete_plan(self, plan_item_id: int) -> None:
        logger.info(f'deleteing plan item with id={plan_item_id}')

        async with self.pool.acquire() as con:
            row = await con.execute('delete from plan where id=$1', plan_item_id)
        logger.info(f'plan item with id={plan_item_id} removed')

    # imports from WD

    async def create_lecture(self, lecture: Lecture) -> Lecture:
        x = lecture  # alias
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('''insert into lectures(przedmiotid, nazwa, active) 
                                               VALUES ($1, $2, $3) returning *''',
                                            x.przedmiotid, x.nazwa, x.active)
            return Lecture(**row)

    async def create_group(self, group: Group) -> Group:
        x = group  # alias
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('''insert into groups(grupaid, nazwa, opis, active) 
                                               VALUES ($1, $2, $3, $4) returning *''',
                                            x.grupaid, x.nazwa, x.opis, x.active)
            return Group(**row)

    async def create_teacher(self, teacher: Teacher):
        x = teacher  # alias
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('''insert into teachers(wykladowcaid, imie, nazwisko, prefix, suffix, active) 
                                               VALUES ($1, $2, $3, $4, $5, $6) returning *''',
                                            x.wykladowcaid, x.imie, x.nazwisko, x.prefix, x.suffix, x.active)
            return Teacher(**row)

    async def get_all_lectures(self) -> list[Lecture]:
        async with self.pool.acquire() as c:
            rows = await c.fetch('select * from lectures')
            return [Lecture(**row) for row in rows]

    async def get_all_teachers(self) -> list[Teacher]:
        async with self.pool.acquire() as c:
            rows = await c.fetch('select * from teachers')
            return [Teacher(**row) for row in rows]

    async def get_all_groups(self) -> list[Group]:
        async with self.pool.acquire() as c:
            rows = await c.fetch('select * from groups')
            return [Group(**row) for row in rows]

    async def remove_lecture_group_teacher(self):
        async with self.pool.acquire() as con:
            await con.execute('delete from groups where true')
            logger.warning('all groups removed')
            await con.execute('delete from lectures where true')
            logger.warning('all lectures removed')
            await con.execute('delete from teachers where true')
            logger.warning('all teachers removed')


async def main():
    db = DbService(DATABASE_URL)
    await db.initialize()
    g1 = Group(grupaid=1, nazwa='G1', opis='gg', active=True)
    g2 = Group(grupaid=2, nazwa='G2', opis='gg', active=True)
    # await db.create_group(g1)
    # await db.create_group(g2)
    print(await db.get_all_groups())
    # await db.remove_lecture_group_teacher()


if __name__ == '__main__':
    # print(DATABASE_URL)
    run(main())
