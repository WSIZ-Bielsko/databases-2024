import asyncio
import asyncpg
from asyncpg import Pool
from pydantic import BaseModel

"""

create table summit1(
                       id int primary key,
                       name text not null,
                       altitude real default 0,
                       position_long real default 0,
                       position_lat real default 0
);

"""


class Summit(BaseModel):
    id: int | None
    name: str
    altitude: float
    position_long: float
    position_lat: float


async def connect_db(database_url: str) -> Pool:
    pool = await asyncpg.create_pool(
        database_url, min_size=5, max_size=10, timeout=30, command_timeout=5
    )
    return pool


async def get_summits(pool: Pool) -> list[Summit]:
    async with pool.acquire() as conn:
        rows = await conn.fetch("select * from summits")  # here your SQL ...
        # for row in rows:
        #     print(Summit(**row))  # instancje klasy Summit
        return [Summit(**row) for row in rows]


async def create_summit(pool: Pool, summit: Summit) -> Summit:
    async with pool.acquire() as conn:
        res = await conn.fetchrow(
            """INSERT INTO summits
            (name, altitude, position_long, position_lat)
            VALUES ($1, $2, $3, $4) returning *""",
            summit.name,
            summit.altitude,
            summit.position_long,
            summit.position_lat,
        )
        return Summit(**res)


async def update_summit(pool: Pool, summit: Summit):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE summits
            SET name = $1, altitude = $2, position_long = $3, position_lat = $4
            WHERE id = $5
        """,
            summit.name,
            summit.altitude,
            summit.position_long,
            summit.position_lat,
            summit.id,
        )


async def delete_summit(pool: Pool, summit_id: int) -> Summit:
    async with pool.acquire() as conn:
        res = await conn.fetchrow(
            "DELETE FROM summits" "WHERE id=$1 RETURNING *", summit_id
        )
        return Summit(**res)


async def main():
    DATABASE_URL = "postgres://postgres:postgres@10.10.1.200:5432/postgres"
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print("db connected")

    lonelyMountain = Summit(
        id=None,
        name="Lonely Mountain 4",
        altitude=441.55,
        position_long=45.1234,
        position_lat=67.9854,
    )

    x = await create_summit(pool, lonelyMountain)
    print(f"result of writing to db: {x=}")

    x.altitude = 1500
    await update_summit(pool, x)

    # x_deleted = await delete_summit(pool, x.id)
    # print(f'deleted: {x_deleted}')

    summits = await get_summits(pool)
    print(summits)
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())  # uruchamia funkcję app ↑↑
