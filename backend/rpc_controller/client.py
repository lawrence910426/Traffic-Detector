from concurrent import futures

import grpc
import proto.interface_pb2 as interface_pb2
import proto.interface_pb2_grpc as interface_pb2_grpc

class RpcClient:
    def __init__(self):
        self.state = "INIT"
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = interface_pb2_grpc.RouteGuideStub(self.channel)
    
    def __del__(self):
        self.channel.close()

    def Init_Task(self):
        success = self.stub.Init_Task(interface_pb2.Parameter(
            Mode=interface_pb2.Parameter.STRAIGHT,
            X=interface_pb2.Parameter.Detector_Line(x1=0, y1=0, x2=0, y2=0),
            Y=interface_pb2.Parameter.Detector_Line(x1=0, y1=0, x2=0, y2=0),
            Z=interface_pb2.Parameter.Detector_Line(x1=0, y1=0, x2=0, y2=0),
            Stabilization_Period=30,
            Input_Video_Path="",
            Output_Video_Path="",
            Log_Path="",
            Start_Time=0,
            End_Time=0,
            Buffer_Time=0
        ))
        self.state = "RUNNING"
        return success
    
    def Get_Task(self):
        task_result = self.stub.Get_Task(interface_pb2.Empty())
        self.state = "COMPLETED" if task_result.Progress == 1.0 else "RUNNING"
        return task_result
    
    def Kill_Task(self):
        success = self.stub.Kill_Task(interface_pb2.Empty())
        self.state = "COMPLETED"
        return success