#!/bin/bash

if [ -z $1 ]
then
	echo "Usage: ./crop [Input] [Output] [Start (in hour)] [End (in hour)]"
	echo "./crop in.mp4 out.mp4 1 2"
	exit
fi

ffmpeg -i $1 -ss $3:00:00 -to $4:00:00 -c:v copy -c:a copy $2
