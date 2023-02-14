echo "GPU_LOCALHOST = $GPU_LOCALHOST"
envsubst '${GPU_LOCALHOST}' < nginx_template.conf > nginx.conf
