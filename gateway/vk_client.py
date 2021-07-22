import asyncio
import inspect
from asyncio import sleep

from vk.fetch import Session
import logging
import settings
import vk
from database import get_group_query, get_user_query, get_subscribers_query
from logger import LOGGER
import re


class VkApi:
    _db = None

    def __init__(self, api, db):
        self._api = vk.Api(api)
        self._db = db

    async def get_info_from_group(self, group):
        info = self._api.get_group(group)
        object_dict = dict()
        for i in dir(info):
            if i in settings.GROUPS_FIELDS.keys():
                value = getattr(info, i)
                object_dict[i] = value
        object_dict['vk_id'] = object_dict['id']
        object_dict.pop('id')
        LOGGER.info('info about ' + group + ' returned')
        return object_dict

    async def get_groups_data(self):
        groups = settings.GROUPS
        LOGGER.info('Selected ' + str(len(groups)) + 'env file')
        info = list()
        for group in groups:
            info.append(await self.get_info_from_group(group=group))
        await self.group_to_db(info)

    async def group_to_db(self, all_data):
        for data in all_data:
            columns = await self.get_query_columns(data.keys())
            values = tuple(data.values())
            keys = '(vk_id)'
            query = get_group_query(columns=columns, values=values, keys=keys)
            await self._db.execute(query)
            LOGGER.info('Upserted row about groups')

    async def get_subscribers(self):
        groups = settings.GROUPS
        tasks = []
        for group in groups:
            while True:
                try:
                    info = self._api.get_group(group)
                    task = asyncio.create_task(self.get_all_users(info.get_members(), info.id))
                    tasks.append(task)
                except Exception as error:
                    LOGGER.warn(error)
                    continue
                break
        await asyncio.gather(*tasks)

    async def get_all_users(self, users: Session.fetch_items, group_vk_id):
        object_list = list()
        i = 0
        for user in users:
            object_dict = dict()
            for attr_ in dir(user):
                if attr_ in settings.USERS_FIELDS:
                    value = getattr(user, attr_)
                    if isinstance(value, str):
                        value = re.sub('[^а-яА-Яa-zA-Z]', '', value)
                    await sleep(0.1)
                    object_dict[attr_] = value

            if i == settings.BATCH_SIZE:
                await self.users_to_db(object_list, group_vk_id)
                object_list.clear()
                i = 0
            i += 1
            object_dict['vk_id'] = object_dict['id']
            object_dict.pop('id')
            object_list.append(object_dict)
        LOGGER.info('All subscribers with group_id ' + str(group_vk_id) + ' are collected')
        await self.users_to_db(object_list, group_vk_id)
    
    async def users_to_db(self, users_list, group_id):
        columns = await self.get_query_columns(users_list[0].keys())
        keys = '(vk_id)'
        values = ''
        for data in users_list:
            values += str(tuple(data.values()))
            values += ','
        values = values[:-1]
        query = get_user_query(columns=columns, values=values, keys=keys)
        await self._db.execute(query)
        LOGGER.info(str(len(users_list)) + ' users are upserted from group with group_id ' + str(group_id))
        values = ''
        for data in users_list:
            values += str(tuple([group_id, list(data.values())[-1]]))
            values += ','
        values = values[:-1]
        query = get_subscribers_query(values)
        LOGGER.info(str(len(users_list)) + ' subscribing relationships are upserted')
        await self._db.execute(query)

    async def get_query_columns(self, keys):
        columns = '('
        for k in keys:
            columns += k
            columns += ','
        columns = columns[:-1]
        columns += ')'
        return columns