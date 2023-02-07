from concurrent import futures
import grpc
import proto.interface_pb2 as interface_pb2
import proto.interface_pb2_grpc as interface_pb2_grpc

from server import RouteGuideServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    interface_pb2.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()