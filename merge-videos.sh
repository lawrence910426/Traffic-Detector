#!/bin/bash

# Merge videos in current directory
ls -1 * | awk '/\.TS/{print "file " $0}' > filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mkv
