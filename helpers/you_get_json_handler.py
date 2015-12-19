#! /usr/bin/env python3
# coding: utf8

import subprocess as sb
import json
import shlex
import sys
from .utils import check_cmd
from .utils import debug,set_debug

DEBUG=False

# check command
if not check_cmd('you-get'):
    raise ImportError("Cannot found you-get in Path")

def handler(url,src=None):
    u'''打包处理函数'''
    data = handler_command(url)
    obj = handler_json(data)
    info = extract_urls(obj)
    debug(info)
    return info

def handler_command(url, encoding="utf8"):
    u'''通过 ``you-get --json`` 获得相关下载内容'''
    cmd = "you-get --json " + shlex.quote(url)
    args = shlex.split(cmd)
    debug(args)
    # return output data. -> b'string'
    # 如果下载超时（60s）报错退出
    # TODO 更好的修正下载
    try:
        data = sb.check_output(args,timeout=60)
    except sb.TimeoutExpired as err:
        print("command run timeout")
        print(err)
        sys.exit(1)
    except sb.CalledProcessError as err:
        print("Called Process Error")
        print(err)
        sys.exit(1)
    # 编码转换
    # TODO 可能在某些终端不转化更好，需要you-get json部分patch safe_ascii
    data_u = data.decode(encoding)
    #debug(data_u)
    return data_u

def handler_json(data):
    u'''从输出生成 json 对象'''
    debug("Try decode json data")
    try:
        json_obj = json.loads(data)
    except json.JSONDecodeError as err:
        print(err)
        sys.exit(1)
    return json_obj

def extract_urls(json_obj):
    u'''解析 json 对象， 获取下载url和后缀'''
    debug("extract useful data")
    streams = json_obj["streams"]
    #for profile in streams:
        #debug("find stream {}".format(profile))
        #down_urls = streams[profile]["src"]
        #debug(down_urls)
    profile = "__default__"
    #debug("find stream {}".format(profile))
    video_format = streams[profile]["container"]
    #debug(video_format)
    video_size = streams[profile]["size"]
    #debug(video_size)
    down_urls = streams[profile]["src"]
    #debug(down_urls)

    # TODO dirty return
    return down_urls,video_format,video_size

if __name__=="__main__":
    DEBUG=True
    url = "http://www.bilibili.com/video/av2807449/index_4.html"
    debug(handler(url))


