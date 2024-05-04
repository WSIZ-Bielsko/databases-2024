from asyncio import run

from wd_proxy import WdProxy
from db_service import DbService, DATABASE_URL
from loguru import logger

"""
Code allows to import lecture, teacher and group info from
the WD (wsiz) to the internal database.
"""


async def main():
    db = DbService(DATABASE_URL)
    await db.initialize()
    wdauth = "65c7976e-68b1-456e-abca-dd7cbe3ad0a1"
    wd = WdProxy(wdauth=wdauth, wd_url="https://wddata.wsi.edu.pl")

    await db.remove_lecture_group_teacher()

    logger.info('importing all groups from wd')
    groups = wd.get_groups()
    for g in groups:
        await db.create_group(g)
    logger.info('importing all groups from wd complete')

    logger.info('importing all teachers from wd')
    teachers = wd.get_teachers()
    for t in teachers:
        await db.create_teacher(t)
    logger.info('importing all teachers from wd complete')

    logger.info('importing all lectures from wd')
    lectures = wd.get_lectures()
    for e in lectures:
        await db.create_lecture(e)
    logger.info('importing all lectures from wd complete')

    logger.warning('all teachers, groups and lectures imported from WD')


if __name__ == '__main__':
    run(main())
