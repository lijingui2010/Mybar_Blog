#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from aiohttp import web
from mybar_blog.routes import set_routes


async def init_app():
    app = web.Application()

    set_routes(app)

    return app


def main():
    app = init_app()

    web.run_app(app)


if __name__ == '__main__':
    main()
