cd /etc/nginx
envsubst '${LOCAL_IP}' < nginx_template.conf > nginx.conf
