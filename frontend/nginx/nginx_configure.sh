echo "LOCAL_IP = $LOCAL_IP"
envsubst '${LOCAL_IP}' < nginx_template.conf > nginx.conf
