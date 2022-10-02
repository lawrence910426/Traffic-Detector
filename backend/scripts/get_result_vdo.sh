echo "cd ../video-detector/output/; curl -v -F file=@{id}.mp4 {host}api/upload_result_video; exit" | nc {LOCAL_IP} 8787
