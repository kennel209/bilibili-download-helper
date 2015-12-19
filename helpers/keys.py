#! /usr/bin/env python3
# coding: utf8

from random import choice
import os

APPKEYS=[
        '8e9fc618fbd41e28', # youtebu-dl
        ]


conf = os.path.join(os.path.dirname(os.path.abspath(__file__)),'APPKEYS')
if os.path.isfile(conf):
    with open(conf) as f:
        for l in f:
            APPKEYS.append(l.strip())

# you-get
#APPKEY = '85eb6835b0a1034e',
#APPSEC = '2ad42749773c441109bdc0191257a664'

def get_appkey(i=0,rand=True):
    return choice(APPKEYS) if rand else APPKEYS[i]

