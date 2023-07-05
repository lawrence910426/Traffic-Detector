#!/bin/bash

if [ -z $1 ]
then
	echo "Usage: ./rotate [Input] [Operation (0, 1, 2, 3)] [Output]"
	echo "e.g. ./rotate in.mp4 2 out.mp4"
	echo "Operation description"
	echo "	0: anti-clockwise 90 degress and vertical flip"
	echo "	1: clockwise 90 degree"
	echo "	2: anti-clockwise 90 degree"
	echo "	3: clockwise and vertical flip"
	exit
fi

ffmpeg -i $1 -vcodec libx264 -vf "transpose="+$2 $3
