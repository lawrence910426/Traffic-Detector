# Traffic detector

1. Fill `BACKEND_HOST` with the reverse proxy url (e.g. `http://123.123.123.123/api/`) of flask backend.
2. Fill `GPU_LOCALHOST` with the internal ip address (or the magic dns name) where `docker-gpu-server.yml` resides.
3. Fill `RPC_HOST_LIST` with the detector hostnames defined in `docker-gpu-server.yml`. For example, `traffic-detector-1,traffic-detector-2`.

# Generate proto before docker build
Run `bash init_proto.sh` in `/rpc-backend-detector`.
