#! /usr/bin/env python3
# coding: utf8

from random import choice

APPKEYS=[
        '8e9fc618fbd41e28', # youtebu-dl
        ]

# you-get
#APPKEY = '85eb6835b0a1034e',
#APPSEC = '2ad42749773c441109bdc0191257a664'

def get_appkey(i=0,rand=False):
    return choice[APPKEYS] if rand else APPKEYS[i]

