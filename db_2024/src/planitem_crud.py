"""
perplexity.ai prompt:

write a class PlanItemCRUD with methods for CRUD operations using asyncpg for the following pydantic data class:

class PlanItem(BaseModel):
    id: int | None
    group_id: int
    lecture_id: int
    teacher_id: int
    room: str
    hour: time
    day_of_week: str

in each method get the connection via `async with self.pool.acquire() as conn:`.



"""
from asyncio import run

import asyncpg
from pydantic import BaseModel
from datetime import time

from db_2024.src.db_service import DbService, DATABASE_URL


class PlanItem(BaseModel):
    id: int | None
    group_id: int
    lecture_id: int
    teacher_id: int
    room: str
    hour: time
    day_of_week: str


class PlanItemCRUD:
    def __init__(self, pool):
        self.pool = pool

    async def create_plan_item(self, plan_item: PlanItem):
        async with self.pool.acquire() as conn:
            query = "INSERT INTO plan_items (group_id, lecture_id, teacher_id, room, hour, day_of_week) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id"
            record = await conn.fetchrow(query, plan_item.group_id, plan_item.lecture_id, plan_item.teacher_id,
                                         plan_item.room, plan_item.hour, plan_item.day_of_week)
            return record['id']

    async def get_plan_item(self, plan_item_id: int):
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM plan_items WHERE id = $1"
            record = await conn.fetchrow(query, plan_item_id)
            return record

    async def update_plan_item(self, plan_item_id: int, new_plan_item: PlanItem):
        async with self.pool.acquire() as conn:
            query = "UPDATE plan_items SET group_id=$1, lecture_id=$2, teacher_id=$3, room=$4, hour=$5, day_of_week=$6 WHERE id=$7"
            await conn.execute(query, new_plan_item.group_id, new_plan_item.lecture_id,
                               new_plan_item.teacher_id, new_plan_item.room,
                               new_plan_item.hour, new_plan_item.day_of_week,
                               plan_item_id)

    async def delete_plan_item(self, plan_item_id: int):
        async with self.pool.acquire() as conn:
            query = "DELETE FROM plan_items WHERE id = $1"
            await conn.execute(query, plan_item_id)


async def main():
    db = DbService(DATABASE_URL)
    await db.initialize()

    pool = db.pool
    repo = PlanItemCRUD(pool)
    item = PlanItem(id=111, group_id=12, lecture_id=88, teacher_id=115, room='S91', hour='12:00', day_of_week='Fri')
    await repo.create_plan_item(item)

    g = await repo.get_plan_item(plan_item_id=1)
    print(g)
    # z = await repo.delete_plan_item(plan_item_id=111)
    # print(z)  # None
    # g = await repo.get_plan_item(plan_item_id=111)
    # print(g)  # None


if __name__ == '__main__':
    # print(DATABASE_URL)
    run(main())
