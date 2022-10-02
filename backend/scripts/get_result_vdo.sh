echo "cd ../video-detector/output/; curl -v -F filename={id}.avi -F file=@{id}.avi {host}api/upload_result_video; exit" | nc {LOCAL_IP} 8787
