import os
from concurrent import futures

import grpc
from google.protobuf import empty_pb2 as wrappers
from .proto import interface_pb2
from .proto import interface_pb2_grpc

class RpcClient:
    def __init__(self, host):
        self.state = "INIT"
        self.channel = grpc.insecure_channel(f"{host}:10000")
        self.stub = interface_pb2_grpc.RouteGuideStub(self.channel)
    
    def __del__(self):
        self.channel.close()

    def Init_Task(self, params):
        success = self.stub.Init_Task(interface_pb2.Parameter(
            Traffic_Mode={
                "straight": interface_pb2.Parameter.STRAIGHT,
                "t_intersection": interface_pb2.Parameter.T_INTERSECTION,
                "cross_intersection": interface_pb2.Parameter.CROSS_INTERSECTION
            }[params["Mode"]],
            X=interface_pb2.Parameter.Detector_Line(
                x1=int(params['X']['x1']), y1=int(params['X']['y1']), 
                x2=int(params['X']['x2']), y2=int(params['X']['y2'])
            ),
            Y=interface_pb2.Parameter.Detector_Line(
                x1=int(params['Y']['x1']), y1=int(params['Y']['y1']), 
                x2=int(params['Y']['x2']), y2=int(params['Y']['y2'])
            ),
            T=interface_pb2.Parameter.Detector_Line(
                x1=int(params['T']['x1']), y1=int(params['T']['y1']), 
                x2=int(params['T']['x2']), y2=int(params['T']['y2'])
            ),
            A=interface_pb2.Parameter.Detector_Line(
                x1=int(params['A']['x1']), y1=int(params['A']['y1']), 
                x2=int(params['A']['x2']), y2=int(params['A']['y2'])
            ),
            B=interface_pb2.Parameter.Detector_Line(
                x1=int(params['B']['x1']), y1=int(params['B']['y1']), 
                x2=int(params['B']['x2']), y2=int(params['B']['y2'])
            ),
            Stabilization_Period=params["Stabilization_Period"],
            Input_Video_Path=params["Input_Video_Path"],
            Output_Video_Path=params["Output_Video_Path"],
            Start_Frame=int(params["Start_Frame"]),
            End_Frame=int(params["End_Frame"])
        ))
        self.state = "RUNNING"
        return success
    
    def Get_Task(self):
        task_result = self.stub.Get_Task(wrappers.Empty())
        if task_result.Progress == 1.0:
            print(task_result)
        self.state = "COMPLETED" if task_result.Progress == 1.0 else "RUNNING"
        return task_result
    
    def Kill_Task(self):
        success = self.stub.Kill_Task(wrappers.Empty())
        self.state = "COMPLETED"
        return success
    
    def Get_State(self):
        return self.state