import asyncpgsa
from asyncpg import exceptions
from logger import LOGGER



class DatabaseClient:
    _instance = None
    _initialized = False
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseClient, cls).__new__(cls)
            cls._instance._initialized = True
        return cls._instance

    async def connect(self, dsn, max_size=20, timeout=60, **kwargs):
        try:
            self._pool = await asyncpgsa.create_pool(dsn, max_size=max_size, command_timeout=timeout, **kwargs)
            LOGGER.info('Database connected')
        except (exceptions.InvalidCatalogNameError, exceptions.InvalidPasswordError,
                ConnectionRefusedError, OSError, ValueError) as error:
            raise error

    async def close(self):
        await self._pool.close()

    async def execute(self, sql):
        try:
            async with self._pool.acquire() as connection:
                return await connection.execute(sql)
        except Exception as error:
            LOGGER.error(error)


    async def fetch_val(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.fetchval(sql)

    async def fetch_one(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(sql)

    async def fetch_all(self, sql):
        async with self._pool.acquire() as connection:
            return await connection.fetch(sql)

    @property
    def pool(self):
        return self._pool


async def run_database_client(dsn):
    LOGGER.info('Starting DB client.')
    client = DatabaseClient()
    await client.connect(dsn)


async def close_database_client():
    LOGGER.info('Stopping DB client.')
    client = DatabaseClient()
    await client.close()


def get_client():
    return DatabaseClient()
