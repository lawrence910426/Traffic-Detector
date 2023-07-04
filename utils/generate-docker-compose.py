REPLICAS = 1

links = "\n".join([f"      - detector_{i}" for i in range(1, REPLICAS + 1)])
host_list = ",".join([f"detector_{i}" for i in range(1, REPLICAS + 1)])
gen_count = False

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
      - $PWD/storage:/mnt/video-in
      - $PWD/storage:/mnt/video-out
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
    shm_size: '32gb'
    volumes:
      - $PWD/storage:/app/video-detector/videos
      - $PWD/storage:/app/video-detector/output
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              { "count: 1" if gen_count else "" }
              capabilities: [gpu]"""
    for i in range(1, REPLICAS + 1)
])

print(backend + workers)
