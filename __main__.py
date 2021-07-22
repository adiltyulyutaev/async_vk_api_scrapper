import asyncio

from database import DatabaseClient
import settings
from gateway import VkApi

db = DatabaseClient()
vk = VkApi(settings.VK_API, db=db)


async def main():
    await db.connect(settings.DATABASE_URL)
    await vk.get_groups_data()
    await vk.get_subscribers()

if __name__ == '__main__':
    asyncio.run(main())
