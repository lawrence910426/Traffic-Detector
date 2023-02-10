pip install grpcio-tools
python -m grpc_tools.protoc \
	-I. --python_out=. --pyi_out=. --grpc_python_out=. \
	interface.proto

cd ..
cp -Lr proto_link proto