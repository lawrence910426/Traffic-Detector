import os
from concurrent import futures

import grpc
from rpc_server.proto import interface_pb2
from rpc_server.proto import interface_pb2_grpc

from rpc_server.server import RouteGuideServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    interface_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    port = os.environ['RPC_PORT']
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()