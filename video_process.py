#! /usr/bin/env python3
# coding: utf8

import sys
import os

import subprocess
import shlex

from utils import check_cmd

DEBUG=False

def debug(s,out=sys.stdout):
    '''common DEBUG function, depend on Glogal DEBUG'''
    if DEBUG:
        print("DEBUG: {!s}".format(s),file=out)

def set_debug(flag):
    '''SET DEBUG flag recursively'''
    global DEBUG
    DEBUG = flag

def make_merge_filelist(parts,outfile='temp.merge'):
    u'''write tempfile to generate filelist for merge'''
    with open(outfile, 'w') as out:
        for part in parts:
            out.write('file ')
            out.write(shlex.quote(part))
            out.write('\n')

    return outfile

def merge_flv(cli,video_parts,output):
    u'''use ffmpeg to merge flv video'''

    if not cli:
        return False

    tempfile = make_merge_filelist(video_parts,output+".merge")
    cmd =  " ".join([cli,
                    "-f concat -i", 
                    shlex.quote(tempfile),
                    "-c copy",
                    shlex.quote(output)])
    debug(cmd)
    args = shlex.split(cmd)
    # TODO non-blocking
    subprocess.call(args)

    os.remove(tempfile)

    return True

def merge_video(ext,video_parts,output):
    u'''wrapper function to dispatch'''

    if check_cmd('ffmpeg'):
        cli = 'ffmpeg'
    elif check_cmd('avconv'):
        cli = 'avconv'
    else:
        print("NO FFmpeg or Avconv Found, skip")
        return False

    if "flv" == ext:
        return merge_flv(cli,video_parts,output)
    else:
        print("Ext format NOT support now, skip")
        return False

if __name__ == "__main__":
    set_debug(True)
    parts = ['【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[00].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[01].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[02].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[03].flv']
    output = '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.flv'
    merge_video("flv",parts,output)

                    
