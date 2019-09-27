#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from mybar_blog.views import index


def set_routes(app):
    app.router.add_get('/', index, name='index')