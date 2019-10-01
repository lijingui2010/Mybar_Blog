#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import time, uuid
from datetime import datetime
from sqlalchemy import MetaData, Table, Column, String, Boolean, Text, DateTime, ForeignKey
import aiomysql.sa


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


meta_data = MetaData()

users = Table(
    'users', meta_data,
    Column('id', String(50), primary_key=True, nullable=False, default=next_id),
    Column('username', String(64), unique=True, nullable=False),
    Column('password', String(128), nullable=False),
    Column('email', String(120), unique=True, nullable=False),
    Column('admin', Boolean, nullable=False, default=False),
    Column('image', String(500), nullable=False),
    Column('timestamp', DateTime, index=True, default=datetime.utcnow)
)

posts = Table(
    'posts', meta_data,
    Column('id', String(50), primary_key=True, nullable=False, default=next_id),
    Column('title', Text, nullable=False),
    Column('content', Text, nullable=False),
    Column('timestamp', DateTime, index=True, default=datetime.utcnow),

    Column('user_id', String(50), ForeignKey('users.id'))
)

comments = Table(
    'comments', meta_data,
    Column('id', String(50), primary_key=True, nullable=False, default=next_id),
    Column('content', Text, nullable=False),
    Column('timestamp', DateTime, default=datetime.utcnow),

    Column('user_id', String(50), ForeignKey('users.id')),
    Column('post_id', String(50), ForeignKey('posts.id'))
)


async def init_engine(config):
    global __engine
    __engine = await aiomysql.sa.create_engine(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        db=config['db_name'],
        charset=config['charset'],
        minsize=config['minsize'],
        maxsize=config['maxsize'],
        autocommit=True
    )
    print('Init DB Engine!')
    return __engine


async def close_engine():
    global __engine
    __engine.close()
    await __engine.wait_closed()
    print('Close DB Engine!')


async def get_users():
    async with __engine.acquire() as conn:
        result_proxy = await conn.execute(users.select().order_by(users.c.id))
        records = await result_proxy.fetchall()
        return records


if __name__ == '__main__':
    import asyncio
    from mybar_blog.settings import get_config, ADMIN_CONFIG_PATH, USER_CONFIG_PATH

    admin_db_config = get_config(ADMIN_CONFIG_PATH)['database']
    user_db_config = get_config(USER_CONFIG_PATH)['database']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_engine(user_db_config))
    rows = loop.run_until_complete(get_users())
    for row in rows:
        print(row)
        print(row['id'])
