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

def make_merge_filelist(parts,outfile='temp.merge'):
    u'''write tempfile to generate filelist for merge'''
    with open(outfile, 'w') as out:
        for part in parts:
            out.write('file ')
            out.write(shlex.quote(part))
            out.write('\n')

    return outfile

def merge_flv(video_parts,output):
    u'''use ffmpeg to merge flv video'''
    tempfile = make_merge_filelist(video_parts,output+".merge")
    cmd =  " ".join(["ffmpeg -f concat -i", 
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
    if "flv" == ext:
        return merge_flv(video_parts,output)
    else:
        print("Ext format NOT support now, skip")
        return False

if __name__ == "__main__":
    set_debug(True)
    parts = ['【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[00].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[01].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[02].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[03].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[04].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[05].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[06].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[07].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[08].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[09].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[10].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[11].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[12].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[13].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[14].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[15].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[16].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[17].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[18].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[19].flv']
    output = '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.flv'
    merge_video("flv",parts,output)

                    
