import threading

import grpc
import proto.interface_pb2 as interface_pb2
import proto.interface_pb2_grpc as interface_pb2_grpc

from ..utils.parser import get_config
from ..traffic_counter import TrafficCounter

class RouteGuideServicer(interface_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        self.running_thread = None
        self.JsonFlow = ""
        self.Progress = 0.0
        self.Output_Video_Path = ""

    def Init_Task(self, request, context):
        args = {
            "Stabilization_Period": request.Stabilization_Period
        }
        self.counter = TrafficCounter(get_config(), args, request.Input_Video_Path)
        self.Output_Video_Path = request.Output_Video_Path

        self.background_thread = threading.Thread(target=self.Run_Task)
        self.background_thread.start()

        return interface_pb2.BoolValue(value=True)

    def Get_Task(self, request, context):
        return interface_pb2.Result(
            JsonFlow=self.JsonFlow,
            Progress=self.Progress,
            Output_Video_Path=self.Output_Video_Path
        )

    def Kill_Task(self, request, context):
        if not self.counter is None:
            del self.counter
        self.counter = None
        return interface_pb2.BoolValue(value=True)

    def Run_Task(self):
        # Assume cross thread communication is safe
        self.counter.init_loop()
        while not self.counter is None:
            try:
                self.Progress = self.counter.run()
            except:
                break
        
        # Finalize the loop
        if not self.counter is None:
            self.JsonFlow = self.counter.finalize_loop()
            del self.counter
