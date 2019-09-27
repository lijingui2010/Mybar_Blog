#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'admin_config.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)

    return config
