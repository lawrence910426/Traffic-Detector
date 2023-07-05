# Traffic detector

1. Fill `BACKEND_HOST` with the reverse proxy url (e.g. `http://123.123.123.123/api/`) of flask backend.
2. Fill `GPU_LOCALHOST` with the gpu server dns name (e.g. `123.123.123.123`)
3. Fill `NEXTCLOUD_HOST` with the nextcloud server dns name (e.g. `http://123.123.123.123:8080`)

# Generate proto before docker build
Run `bash init_proto.sh` in `/rpc-backend-detector`.
