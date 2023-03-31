# Move all videos to total
rm -r total
mkdir total
mv */*.TS total
cd total

# Generate video
ls -1 * | awk '/\.TS/{print "file " $0}' > filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mkv

# Crop to smaller parts for youtube
ffmpeg -i output.mkv -ss 00:00:00 -to 10:00:00 -c:v copy -c:a copy part_1.mp4
ffmpeg -i output.mkv -ss 10:00:00 -to 20:00:00 -c:v copy -c:a copy part_2.mp4
ffmpeg -i output.mkv -ss 20:00:00 -to 30:00:00 -c:v copy -c:a copy part_3.mp4

# Rotate video
ffmpeg -i output.mkv -vf "transpose=0" rotated.mkv # anti-clockwise 90 degress and vertical flip
ffmpeg -i output.mkv -vf "transpose=1" rotated.mkv # clockwise 90 degree
ffmpeg -i output.mkv -vf "transpose=2" rotated.mkv # anti-clockwise 90 degree
ffmpeg -i output.mkv -vf "transpose=3" rotated.mkv # clockwise and vertical flip
