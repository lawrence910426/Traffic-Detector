pip install grpcio-tools
python -m grpc_tools.protoc \
	-I. --python_out=../backend/routes/rpc_controller/proto \
	--pyi_out=../backend/routes/rpc_controller/proto \
	--grpc_python_out=../backend/routes/rpc_controller/proto \
	interface.proto

python -m grpc_tools.protoc \
	-I. --python_out=../video-detector/rpc_server/proto \
	--pyi_out=../video-detector/rpc_server/proto \
	--grpc_python_out=../video-detector/rpc_server/proto \
	interface.proto
