#! /usr/bin/env python3
# coding: utf8

import sys
import os
import subprocess
import shlex
from .utils import check_cmd
from .utils import debug,set_debug

DEBUG=False

def make_merge_filelist(parts,outfile='temp.merge'):
    u'''write tempfile to generate filelist for merge'''
    with open(outfile, 'w') as out:
        for part in parts:
            out.write('file ')
            # escape single quote
            out.write("'"+part.replace("'","'\\''")+"'")
            out.write('\n')

    return outfile

def merge_flv(cli,video_parts,output,to_ext='flv'):
    u'''use ffmpeg to merge flv video'''

    if not cli:
        return False

    # suppress FFmpeg info
    if not DEBUG:
        LOGLEVEL = '-loglevel quiet'
    else:
        LOGLEVEL = ''

    # NOTE: ffmpeg require concat input file to be in top directory
    #       use basename to remove any os separator
    # FIXME: escape ":" ?
    tempfile = make_merge_filelist(video_parts,os.path.basename(output).replace(":","_")+".merge")
    output = ".".join([output,to_ext])

    cmd =  " ".join([cli,
                    LOGLEVEL,
                    "-f concat -i",
                    shlex.quote(tempfile),
                    "-c copy",
                    shlex.quote(output)])
    debug(cmd)
    args = shlex.split(cmd)

    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as err:
        print(err)
        print("Some Error Occured in Merge {}".format(output))
        print("You should clean up tempfile youself")
        return False
    finally:
        os.remove(tempfile)

    return True

def merge_video(ext,video_parts,output,to_ext='flv'):
    u'''wrapper function to dispatch'''

    if check_cmd('ffmpeg'):
        cli = 'ffmpeg'
    elif check_cmd('avconv'):
        cli = 'avconv'
    else:
        print("NO FFmpeg or Avconv Found, skip")
        return False

    if "flv" == ext and ( "flv" == to_ext or "mp4" == to_ext ):
        if ext == to_ext and len(video_parts) <= 1:
            print("No NEED to convert {}".format(ext))
            return True
        return merge_flv(cli,video_parts,output,to_ext)
    else:
        print("Ext format NOT support now, skip")
        return False

if __name__ == "__main__":
    set_debug(True)
    parts = ['【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[00].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[01].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[02].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[03].flv']
    output = '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.flv'
    merge_video("flv",parts,output)


