#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://docs.ocean.dwavesys.com/en/latest/overview/dwavesys.html#querying-available-solvers

from dwave.cloud import Client
client = Client.from_config(token='DEV-857f7cdd7b520a297ee602765add3ba6964b45b2')

print(client.get_solvers())

# update: ~/.config/dwave
