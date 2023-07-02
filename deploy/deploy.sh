# Build frontend
cd ../frontend
docker build -t lawrence910426/traffic-frontend .

# Build backend
cd ../backend
docker build -t lawrence910426/traffic-backend .

# Build detector
cd ../video-detector
docker build -t lawrence910426/traffic-detector .

# Push to gcr.io
docker push lawrence910426/traffic-backend
docker push lawrence910426/traffic-frontend
docker push lawrence910426/traffic-detector
