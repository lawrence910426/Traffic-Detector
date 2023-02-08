# Traffic detector

1. Fill `BACKEND_HOST` with the reverse proxy url (e.g. `http://123.123.123.123/api/`) of flask backend.
2. Fill `GPU_LOCALHOST` with the internal ip address (or the magic dns name) where `docker-gpu-server.yml` resides.
3. Fill `RPC_PORT_1` with the RPC port of 1st replica.
4. Fill `RPC_PORT_LIST` with port list. (e.g. `5001,5002,5003`)