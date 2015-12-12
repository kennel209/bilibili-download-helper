#! /usr/bin/env python3
# coding: utf8

import sys
import os

import subprocess
import shlex

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag

def check_cmd(cli):
    u'''use subprocess to check cmd'''
    cmd = "which " + shlex.quote(cli)
    debug(cmd)

    try:
        subprocess.check_output(shlex.split(cmd))
        return True
    except subprocess.CalledProcessError as err:
        return False

    print('weird, check cmd error')
    sys.exit(1)

