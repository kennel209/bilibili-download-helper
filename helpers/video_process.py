#! /usr/bin/env python3
# coding: utf8

import sys
import os
import subprocess
import shlex
import random
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
    u'''use ffmpeg concat to merge video'''

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
    tempfile = make_merge_filelist(video_parts,"."+os.path.basename(output).replace(":","_")+".merge")
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

def merge_mp4(cli,video_parts,output,to_ext='mp4'):
    u'''use ffmpeg to merge mp4'''

    if not cli:
        return False

    # suppress FFmpeg info
    if not DEBUG:
        LOGLEVEL = '-loglevel quiet'
    else:
        LOGLEVEL = ''

    # FIXME: quick random filename prefix
    ts_prefix = str(random.randint(999999))
    ts_parts = []
    try:
        for i,video in enumerate(video_parts):
            root,ext = os.path.splitext(video)
            if ext != "mp4":
                print("WARNING: Not .mp4, anyway,contine")

            # NOTE: ffmpeg -i 1.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb 1.ts
            # prepare fo concat:0.ts|1.ts
            ts = "{}_{}.ts".format(ts_prefix,i)

            cmd =  " ".join([cli,
                            LOGLEVEL,
                            "-i",
                            shlex.quote(video),
                            "-c copy  vbsf h264_mp4toannexb",
                            shlex.quote(ts)])
            debug(cmd)
            args = shlex.split(cmd)

            try:
                subprocess.check_call(args)
                ts_parts.append(ts)
            except subprocess.CalledProcessError as err:
                print(err)
                print("Some Error Occured in Converting {}".format(output))
                print("You should clean up tempfile youself")
                if os.path.isfile(ts):
                    os.remove(ts)
                return False

        # NOTE: ffmpeg -i "concat:1.ts|2.ts" -acodec copy -vcodec copy -absf aac_adtstoasc output.mp4
        output = ".".join([output,to_ext])
        concat = "|".join(ts_parts)
        concat = "concat:"+concat

        cmd =  " ".join([cli,
                        LOGLEVEL,
                        "-i",
                        concat,
                        "-c copy -absf aac_adtstoasc",
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
        for ts in ts_parts:
            if os.path.isfile(ts):
                os.remove(ts)

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

    if ("flv" == ext or 'mp4' == ext ) and ( "flv" == to_ext or "mp4" == to_ext ):
        if ext == to_ext and len(video_parts) <= 1:
            print("No NEED to convert {}".format(ext))
            return True
        if "flv" == ext:
            return merge_flv(cli,video_parts,output,to_ext)
        elif "mp4" == ext and "mp4" == to_ext:
            return merge_mp4(cli,video_parts,output,to_ext)
    else:
        print("Ext format NOT support now, skip")
        return False

if __name__ == "__main__":
    set_debug(True)
    parts = ['【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[00].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[01].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[02].flv', '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音.[03].flv']
    output = '【Vmoe字幕組】LiSA演唱会 ~LOVER"S"MiLE~ in 日比谷野音'
    merge_video("flv",parts,output)


