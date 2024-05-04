import os
from asyncio import run

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from model import PlanItem, Group, Teacher
from pydantic import BaseModel

load_dotenv()  # take environment variables from .env.

DEFAULT_DATABASE_URL = "postgres://postgres:postgres@10.10.1.200:5432/postgres"

DATABASE_URL = os.getenv("DB_URL", DEFAULT_DATABASE_URL)


class Lecture(BaseModel):
    przedmiotid: int
    nazwa: str
    active: bool


class LectureCRUD:
    def __init__(self, pool):
        self.pool = pool

    async def create_lecture(self, lecture: Lecture):
        lct = lecture  # alias
        async with self.pool.acquire() as conn:
            query = """
            INSERT INTO lectures (przedmiotid, nazwa, active)
            VALUES ($1, $2, $3) RETURNING *"""
            record = await conn.fetchrow(query, lct.przedmiotid, lct.nazwa, lct.active)
            return Lecture(**record)

    async def read_lecture(self, przedmiotid: int):
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM lectures WHERE przedmiotid = $1"
            record = await conn.fetchrow(query, przedmiotid)
            return Lecture(**record)

    async def update_lecture(self, przedmiotid: int, new_data: Lecture):
        async with self.pool.acquire() as conn:
            query = """UPDATE lectures
            SET nazwa = $1, active = $2
            WHERE przedmiotid = $3 RETURNING *"""
            record = await conn.fetchrow(
                query, new_data.nazwa, new_data.active, przedmiotid
            )
            return Lecture(**record)

    async def delete_lecture(self, przedmiotid: int):
        async with self.pool.acquire() as conn:
            query = "DELETE FROM lectures WHERE przedmiotid = $1 RETURNING *"
            record = await conn.fetchrow(query, przedmiotid)
            return Lecture(**record)


class DbService:

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=5,
                max_size=10,
                timeout=30,
                command_timeout=5,
            )
            logger.info("database connected!")
        except Exception as e:
            logger.error(f"Error connecting to DB, {e}")

    async def create_plan(self, item: PlanItem):
        logger.info("plan item creating")
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """
            insert into
            plan(group_id,lecture_id,room,hour,day_of_week,teacher_id)
            VALUES ($1, $2, $3, $4, $5, $6) returning *""",
                item.group_id,
                item.lecture_id,
                item.room,
                item.hour,
                item.day_of_week,
                item.teacher_id,
            )
        created = PlanItem(**dict(row))
        logger.info(f"plan item created: {created}")

        return created  # with db-generated id

    async def update_plan(self, item: PlanItem) -> PlanItem:
        logger.info(f"plan item id={item.id} update: {item}")
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """
            update plan set group_id=$2, lecture_id=$3, room=$4, hour=$5,
            day_of_week=$6, teacher_id=$7 where id=$1 returning *""",
                item.id,
                item.group_id,
                item.lecture_id,
                item.room,
                item.hour,
                item.day_of_week,
                item.teacher_id,
            )
        updated = PlanItem(**dict(row))
        logger.info(f"plan item updated: {updated}")
        return updated

    async def delete_plan(self, plan_item_id: int) -> None:
        logger.info(f"deleteing plan item with id={plan_item_id}")

        async with self.pool.acquire() as con:
            await con.execute("delete from plan where id=$1", plan_item_id)
        logger.info(f"plan item with id={plan_item_id} removed")

    # imports from WD

    async def create_lecture(self, lecture: Lecture) -> Lecture:
        x = lecture  # alias
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """
            insert into
            lectures(przedmiotid, nazwa, active)
            VALUES ($1, $2, $3) returning *""",
                x.przedmiotid,
                x.nazwa,
                x.active,
            )
            return Lecture(**row)

    async def create_group(self, group: Group) -> Group:
        x = group  # alias
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """insert into groups(grupaid, nazwa, opis, active)
                VALUES ($1, $2, $3, $4) returning *""",
                x.grupaid,
                x.nazwa,
                x.opis,
                x.active,
            )
            return Group(**row)

    async def create_teacher(self, teacher: Teacher):
        x = teacher  # alias
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                """insert into
            teachers(wykladowcaid, imie, nazwisko,
            prefix, suffix, active)
            VALUES ($1, $2, $3, $4, $5, $6) returning *""",
                x.wykladowcaid,
                x.imie,
                x.nazwisko,
                x.prefix,
                x.suffix,
                x.active,
            )
            return Teacher(**row)

    async def get_all_lectures(self) -> list[Lecture]:
        async with self.pool.acquire() as c:
            rows = await c.fetch("select * from lectures")
            return [Lecture(**row) for row in rows]

    async def get_all_teachers(self) -> list[Teacher]:
        async with self.pool.acquire() as c:
            rows = await c.fetch("select * from teachers")
            return [Teacher(**row) for row in rows]

    async def get_all_groups(self) -> list[Group]:
        async with self.pool.acquire() as c:
            rows = await c.fetch("select * from groups")
            return [Group(**row) for row in rows]

    async def remove_lecture_group_teacher(self):
        async with self.pool.acquire() as con:
            await con.execute("delete from groups where true")
            logger.warning("all groups removed")
            await con.execute("delete from lectures where true")
            logger.warning("all lectures removed")
            await con.execute("delete from teachers where true")
            logger.warning("all teachers removed")

        # generated by https://www.perplexity.ai/
        async def create_lecture(conn, lecture: Lecture):
            query = """INSERT INTO lectures (przedmiotid, nazwa, active)
             VALUES ($1, $2, $3) RETURNING *"""
            record = await conn.fetchrow(
                query, lecture.przedmiotid, lecture.nazwa, lecture.active
            )
            return record

        async def read_lecture(conn, lecture_id: int):
            query = "SELECT * FROM lectures WHERE przedmiotid = $1"
            record = await conn.fetchrow(query, lecture_id)
            return record

        async def update_lecture(conn, lecture_id: int, new_data: Lecture):
            query = """UPDATE lectures SET nazwa = $1, active = $2
            WHERE przedmiotid = $3 RETURNING *"""
            record = await conn.fetchrow(
                query, new_data.nazwa, new_data.active, lecture_id
            )
            return record

        async def delete_lecture(lecture_id: int):
            async with self.pool.acquire() as conn:
                query = """DELETE FROM lectures
                 WHERE przedmiotid = $1 RETURNING *"""
                record = await conn.fetchrow(query, lecture_id)
                return record


async def main():
    db = DbService(DATABASE_URL)
    await db.initialize()
    g1 = Group(grupaid=1, nazwa="G1", opis="gg", active=True)
    g2 = Group(grupaid=2, nazwa="G2", opis="gg", active=True)
    await db.create_group(g1)
    await db.create_group(g2)
    print(await db.get_all_groups())
    await db.remove_lecture_group_teacher()

    pool = db.pool
    lecture_crud = LectureCRUD(pool)
    lecture = Lecture(przedmiotid=2222, nazwa="Kadabra", active=True)
    await lecture_crud.create_lecture(lecture)


if __name__ == "__main__":
    # print(DATABASE_URL)
    run(main())
