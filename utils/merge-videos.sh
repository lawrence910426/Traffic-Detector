# Move all videos to total
rm -r total
mkdir total
mv */*.TS total
cd total

# Generate video
ls -1 * | awk '/\.TS/{print "file " $0}' > filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mkv

# Crop to smaller parts for youtube
ffmpeg -i input.mp4 -ss 00:00:00 -to 10:00:00 -c:v copy -c:a copy part_1.mp4
ffmpeg -i input.mp4 -ss 10:00:00 -to 20:00:00 -c:v copy -c:a copy part_2.mp4
ffmpeg -i input.mp4 -ss 20:00:00 -to 30:00:00 -c:v copy -c:a copy part_3.mp4
