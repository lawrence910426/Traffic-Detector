import os

from concurrent import futures
import grpc
import proto.interface_pb2 as interface_pb2
import proto.interface_pb2_grpc as interface_pb2_grpc

from server import RouteGuideServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    interface_pb2.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    port = os.environ['RPC_PORT']
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()