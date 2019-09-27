#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from aiohttp import web


async def index(request):
    return web.Response(body='<h3>Welcome to Mybar Blog<h3>', content_type='text/html')
