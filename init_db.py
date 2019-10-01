#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

from mybar_blog.settings import get_config, ADMIN_CONFIG_PATH, USER_CONFIG_PATH
from mybar_blog.db import users, posts, comments, next_id


def construct_db_url(config):
    dsn = "{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}?charset={charset}"

    return dsn.format(
        dialect=config['dialect'],
        driver=config['driver'],
        user=config['user'],
        password=config['password'],
        database=config['db_name'],
        host=config['host'],
        port=config['port'],
        charset=config['charset']
    )


def get_engine(config):
    db_url = construct_db_url(config)
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


def setup_db(admin_config=None, user_config=None):
    engine = get_engine(admin_config)

    db_host = user_config['host']
    db_name = user_config['db_name']
    db_user = user_config['user']
    db_password = user_config['password']
    db_charset = user_config['charset']

    if not database_exists(engine.url):
        create_database(engine.url)

    with engine.connect() as conn:
        teardown_db(admin_config=admin_config, user_config=user_config)

        conn.execute("CREATE USER IF NOT EXISTS '%s'@'%s' IDENTIFIED BY '%s'" % (db_user, db_host, db_password))
        conn.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET %s" % (db_name, db_charset))
        conn.execute("GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%s'" % (db_name, db_user, db_host))


def teardown_db(admin_config=None, user_config=None):
    engine = get_engine(admin_config)

    db_host = user_config['host']
    db_name = user_config['db_name']
    db_user = user_config['user']

    if database_exists(engine.url):
        with engine.connect() as conn:
            conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
            conn.execute("DROP USER IF EXISTS '%s'@'%s'" % (db_user, db_host))


def create_tables(config):
    engine = get_engine(config)

    meta_data = MetaData()
    meta_data.create_all(bind=engine, tables=[users, posts, comments])


def drop_tables(config):
    engine = get_engine(config)

    meta_data = MetaData()
    meta_data.drop_all(bind=engine, tables=[users, posts, comments])


def create_sample_data(config):
    engine = get_engine(config)

    with engine.connect() as conn:
        user_id_1 = next_id()
        user_id_2 = next_id()
        conn.execute(users.insert(),
                     [
                         {
                             'id': user_id_1,
                             'username': 'lijingui2010',
                             'password': 'mybar835',
                             'email': 'lijingui2010@mybar.com',
                             'image': 'about:blank'
                         },
                         {
                             'id': user_id_2,
                             'username': 'test',
                             'password': 'test',
                             'email': 'test@163.com',
                             'image': 'about:blank'
                         }
                     ])

        post_id_1 = next_id()
        post_id_2 = next_id()
        conn.execute(posts.insert(),
                     [
                         {
                             'id': post_id_1,
                             'title': 'This is Just a Test!',
                             'content': 'I try to Use Python to construct a Blog application with MySQL storage.',
                             'user_id': user_id_1
                         },
                         {
                             'id': post_id_2,
                             'title': 'Welcome!',
                             'content': 'Welcome my friend!',
                             'user_id': user_id_2
                         }
                     ])

        conn.execute(comments.insert(),
                     [
                         {
                             'content': 'Thanks so much.',
                             'user_id': user_id_1,
                             'post_id': post_id_1
                         },
                         {
                             'content': 'Hello and Thanks.',
                             'user_id': user_id_2,
                             'post_id': post_id_2
                         }
                     ])


if __name__ == '__main__':
    admin_db_config = get_config(ADMIN_CONFIG_PATH)['database']
    user_db_config = get_config(USER_CONFIG_PATH)['database']

    setup_db(admin_config=admin_db_config, user_config=user_db_config)
    create_tables(user_db_config)
    create_sample_data(user_db_config)
    # drop_tables(user_db_config)
