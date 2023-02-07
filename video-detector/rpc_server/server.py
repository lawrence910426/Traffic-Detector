from concurrent import futures
import logging
import math
import time

import grpc
import proto.interface_pb2 as interface_pb2
import proto.interface_pb2_grpc as interface_pb2_grpc


class RouteGuideServicer(interface_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        pass

    def Init_Task(self, request, context):
        print(request.Stabilization_Period)
        return interface_pb2.BoolValue(value=True)

    def Get_Task(self, request, context):
        return interface_pb2.Result(
            JsonFlow="",
            Progress=0.0,
            Output_Video_Path=""
        )

    def Kill_Task(self, request, context):
        return interface_pb2.BoolValue(value=True)

