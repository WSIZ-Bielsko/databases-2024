from uuid import UUID

import asyncpg
from model import *


class SurgeriesRepo:

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    def create_surgery(self, surgery: Surgery):
        pass

    def update_surgery(self, surgery: Surgery):
        pass

    def delete_surgery(self, surgery_id: UUID):
        pass
