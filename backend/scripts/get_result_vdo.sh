echo "cd ../video-detector/output/; curl -s -F file=@{id}.avi {host}upload_result_video; exit" | nc {LOCAL_IP} 8787
