#!/bin/bash

if [ -z $1 ]
then
	echo "Usage: ./esee-convert [output format (mp4, mkv)]"
	echo "e.g. ./esee-convert mp4"
	exit
fi

output_file=out.$1
temp_pos=/tmp/video
# Move all videos to temp
rm -r $temp_pos
mkdir $temp_pos

# Aggregate files for at most 3 layers 
mv *.TS $temp_pos
mv */*.TS $temp_pos
mv */*/*.TS $temp_pos

# Generate video
cd $temp_pos
ls -1 * | awk '/\.TS/{print "file " $0}' > filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mkv
mv output_file $PWD


