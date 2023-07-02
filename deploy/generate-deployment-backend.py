REPLICAS = 6

links = "\n".join([f"      - detector_{i}" for i in range(1, REPLICAS + 1)])
host_list = ",".join([f"detector_{i}" for i in range(1, REPLICAS + 1)])
gen_count = False

before = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend-app
  template:
    metadata:
      labels:
        app: backend-app
    spec:
      volumes:
      - name: video-storage
        persistentVolumeClaim:
          claimName: pvc-video-storage
      containers:
      - name: backend-container
        image: lawrence910426/traffic-backend
        volumeMounts:
          - name: video-storage
            mountPath: /mnt
        envFrom:
          - configMapRef:
              name: rpc-configmap
"""

workers = "\n".join([
    f"""
      - name: detector-container-{i}
        image: lawrence910426/traffic-detector
        volumeMounts:
          - name: video-storage
            mountPath: /mnt
        envFrom:
          - configMapRef:
              name: rpc-configmap
  detector_{i}:
    ipc: host
    container_name: 'traffic-detector-{i}'
    build: 
      context: ./video-detector
    restart: always
    shm_size: '32gb'
    volumes:
      - $PWD/storage/video-in:/app/video-detector/videos
      - $PWD/storage/video-out:/app/video-detector/output
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              { "count: 1" if gen_count else "" }
              capabilities: [gpu]"""
    for i in range(1, REPLICAS + 1)
])

after = """
      restartPolicy: Always
"""

print(before + workers + after)
