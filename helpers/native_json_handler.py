#! /usr/bin/env python3
# coding: utf8

import subprocess as sb
import json
import re
import shlex
import sys
from functools import lru_cache # for memo
#from utils import check_cmd
#from utils import debug,set_debug
#from utils import get_url
#from keys import get_appkey
from .utils import check_cmd
from .utils import debug,set_debug
from .utils import get_url
from .keys import get_appkey

DEBUG=False

APPKEY = get_appkey()
DURL_API = "http://interface.bilibili.com/v_cdn_play?appkey="+APPKEY+"&cid={}"

def get_aid_by_url(url):
    u'''get aid from url, with page if any'''
    # http://www.bilibili.com/video/av1024369/index_01.html
    bili_pattern = re.compile(r'www.bilibili.com/video/av(?P<aid>\d+)/(?:index_(?P<page>\d+).html)?')
    bili_match = bili_pattern.search(url)
    if bili_match is None:
        print("No aid found")
        sys.exit(1)

    aid = bili_match.group("aid")
    page = bili_match.group("page")
    debug("aid={},page={}".format(aid,page))
    return aid,page

@lru_cache(maxsize=None)
def get_pages_info_by_pagelist(aid):
    u'''get page info by pagelist api'''
    PAGELIST_API = "http://www.bilibili.com/widget/getPageList?aid={}"

    page_data = get_url(PAGELIST_API.format(aid))

    try:
        page_json_list = json.loads(page_data)
    except json.JSONDecodeError as err:
        print(err)
        sys.exit(1)
    #debug(page_json_list)

    return page_json_list

@lru_cache(maxsize=None)
def get_av_full_info(aid):
    u'''get av full info, use bilibli api'''
    # get info by aid and page
    #JSON_API = "http://api.bilibili.com/view?type=json&appkey="+APPKEY+"&id={}&page={}"
    # get info by aid only
    JSON_ALL_API = "http://api.bilibili.com/view?type=json&appkey="+APPKEY+"&id={}&batch=1"

    #if page is not None:
    #    av_data = get_url(JSON_API.format(aid,page))
    #else:
    #    av_data = get_url(JSON_ALL_API.format(aid))
    av_data = get_url(JSON_ALL_API.format(aid))

    try:
        av_json_dict = json.loads(av_data)
    except json.JSONDecodeError as err:
        print(err)
        sys.exit(1)
    #debug(av_json_dict)

    if 'error' in av_json_dict:
        print("INFO Fetch Error, {}".format(av_json_dict['error']))

    return av_json_dict

def get_cid_by_av_info(av_json_dict,page=None):
    u'''return cid for certain page or all page'''
    pages = [page_info for page_info in av_json_dict['list']]
    cids = [cid['cid'] for cid in pages]
    if page is None:
        return cids
    else:
        return [cids[int(page)-1]]

def get_cid_by_page_info(page_json_list,page=None):
    u'''return cid for certain page or all page'''
    cids = [cid['cid'] for cid in page_json_list]
    if page is None:
        return cids
    else:
        return [cids[int(page)-1]]

def get_video_info_by_cid(cid,prefer='flv',quality=4):
    u'''get real video link by cid'''
    #URL_API="http://interface.bilibili.com/v_cdn_play?appkey="+APPKEY+"&cid={}"
    URL_API="http://interface.bilibili.com/playurl?appkey="+APPKEY+"&otype=json&cid={}&type={}&quality={}"

    video_info = get_url(URL_API.format(cid,prefer,quality))
    try:
        video_info_dict = json.loads(video_info)
    except json.JSONDecodeError as err:
        print(err)
        sys.exit(1)

    if 'error' == video_info_dict['result']:
        print("Video {} Fetch Error, {}".format(cid,video_info_dict['message']))

    #debug(video_info_dict)
    return video_info_dict

def get_video_info(cids,prefer='flv',quality=4):
    u'''get download list'''
    res = []
    for cid in cids:
        video_format = prefer
        video_info_dict = get_video_info_by_cid(cid,prefer,quality)
        down_urls = []
        video_size = 0
        for durl in video_info_dict['durl']:
            down_urls.append(durl['url'])
            video_size += durl['size'] if 'size' in durl else durl.get('filesize',0)
        #debug(("cid :",cid,down_urls,video_format,video_size))
        res.append((down_urls,video_format,video_size))
    return res

def handler(url):
    u'''打包处理函数'''
    aid,page = get_aid_by_url(url)
    #av_info = get_av_full_info(aid)
    #cids = get_cid_by_av_info(av_info,page)
    page_info = get_pages_info_by_pagelist(aid)
    cids = get_cid_by_page_info(page_info,page)
    debug("cid is {}".format(cids))
    info = get_video_info(cids,'flv','4')
    debug(info)
    # TODO: cid list
    return info[0]

if __name__=="__main__":
    set_debug(True)
    url = "http://www.bilibili.com/video/av1024369/index_02.html"
    url1 = "http://www.bilibili.com/video/av1024369/"
    url2 = "http://www.bilibili.com/video/av3367059/"
    url2 = "http://www.bilibili.com/video/av1036563/"
    #url = "http://www.bilibili.com/video/av2807449/index_4.html"
    #handler(url)
    #handler(url1)
    handler(url2)


