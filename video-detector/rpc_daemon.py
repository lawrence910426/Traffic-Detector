import os
from concurrent import futures
import time

import grpc
from rpc_server.proto import interface_pb2
from rpc_server.proto import interface_pb2_grpc

from rpc_server.server import RouteGuideServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    interface_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    
    server.add_insecure_port(f'[::]:10000')
    server.start()
    print(f"[RPC Server instantiated]")
    time.sleep(1)
    
    # Blocks the main thread from completion
    server.wait_for_termination()

if __name__ == "__main__":
    serve()