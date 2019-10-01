#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from aiohttp import web
from mybar_blog.routes import set_routes
from mybar_blog.settings import get_config, USER_CONFIG_PATH
from mybar_blog.db import init_engine, close_engine


async def on_startup(app):
    engine = await init_engine(app['config']['database'])
    app['engine'] = engine


async def on_shutdown(app):
    await close_engine()


async def init_app(config):
    app = web.Application()

    app['config'] = config

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    set_routes(app)

    return app


def main(config_path):
    config = get_config(config_path)
    app = init_app(config)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    import argparse

    parse = argparse.ArgumentParser()
    parse.add_argument('-c', '--config', help="Provide path to config file", default=USER_CONFIG_PATH)
    args = parse.parse_args()

    if args.config:
        main(args.config)
    else:
        parse.print_help()
