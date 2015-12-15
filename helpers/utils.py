#! /usr/bin/env python3
# coding: utf8

import sys
import os
from urllib.request import urlopen
from urllib.error import URLError
import gzip
import zlib
import subprocess
import shlex

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag,modules=None):
    '''SET DEBUG flag recursively'''
    global DEBUG

    # 消除循环设置
    if debug == flag:
        return

    DEBUG = flag

    if modules is None:
        modules = []
    for m in modules:
        m.set_debug(flag)

def get_url(url,encoding='utf-8'):
    u'''urlopen to getdata'''
    try:
        r = urlopen(url)
        debug((r.geturl(),r.status,r.reason))
        if r.status == 200:
            data = r.read()
            # gzip to decompress
            comp = r.getheader("Content-Encoding") or "none"
            if "gzip" in comp:
                data = gzip.decompress(data)
            elif "deflate" in comp:
                data = zlib.decomporess(data)
            # b'string' -> 'string'
            data_u = data.decode(encoding)
            #debug(data_u)
            return data_u
        else:
            print(r.status,r.reason,"OPEN URL ERROR")
            sys.exit(1)
    except URLError as err:
        print(err)
        sys.exit(1)

def escape_seps(s):
    u'''消除路径分割符号和部分特殊字符'''
    tmp = s.replace(os.sep,"_")
    tmp = tmp.replace(os.linesep,"_")
    tmp = tmp.replace("\0","_")
    return tmp

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

