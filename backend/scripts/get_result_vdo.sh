echo "cd ../video-detector/output/; curl -s -F file=@{id}.mp4 {host}upload_result_video; exit" | nc {LOCAL_IP} 8787
