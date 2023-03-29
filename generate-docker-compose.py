REPLICAS = 16

links = "\n".join([f"      - detector_{i}" for i in range(1, REPLICAS + 1)])
host_list = ",".join([f"detector_{i}" for i in range(1, REPLICAS + 1)])

backend = f"""
version: '3'
services:
  backend:
    ipc: host
    container_name: 'traffic-backend'
    build: ./backend
    restart: always
    ports:
      - 8000:8000
    environment:
      - BACKEND_HOST=${{BACKEND_HOST}}
      - RPC_HOST_LIST={host_list}
    links:
{links}
    volumes:
      - video-in-volume:/mnt/video-in
      - video-out-volume:/mnt/video-out
    deploy:
        resources:
          reservations:
            devices:
              - driver: nvidia
                count: 1
                capabilities: [gpu]

"""

workers = "\n".join([
    f"""
  detector_{i}:
    ipc: host
    container_name: 'traffic-detector-{i}'
    build: 
      context: ./video-detector
    restart: always
    volumes:
      - video-in-volume:/app/video-detector/videos
      - video-out-volume:/app/video-detector/output
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]"""
    for i in range(1, REPLICAS + 1)
])

volumes = """
volumes:
  video-out-volume: 
  video-in-volume:
"""

print(backend + workers + volumes)
