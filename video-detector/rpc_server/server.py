import threading

import grpc
import proto.interface_pb2 as interface_pb2
import proto.interface_pb2_grpc as interface_pb2_grpc

from ..utils.parser import get_config
from ..utils.loop_exception import LoopException
from ..traffic_counter import TrafficCounter

class RouteGuideServicer(interface_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        self.running_thread = None
        self.JsonFlow = ""
        self.Progress = 0.0
        self.Output_Video_Path = ""

    def Init_Task(self, request, context):
        self.Output_Video_Path = "/app/video_detector/output" + request.Output_Video_Path
        args = {
            "mode": request.Mode,
            "detector_line_t": request.Detector_Line_T,
            "detector_line_a": request.Detector_Line_A,
            "detector_line_b": request.Detector_Line_B,
            "detector_line_x": request.Detector_Line_X,
            "detector_line_y": request.Detector_Line_Y,
            "detector_line_z": request.Detector_Line_Z,
            "stable_period": request.Stabilization_Period,
            "output_name": self.Output_Video_Path,
            "start_frame": request.Start_Frame,
            "end_frame": request.End_Frame
        }
        self.counter = TrafficCounter(get_config(), args, 
            "/app/video_detector/videos" + request.Input_Video_Path)

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
                self.Progress = self.counter.loop()
            except LoopException as e:
                break
        
        # Finalize the loop
        if not self.counter is None:
            self.JsonFlow = self.counter.finalize_loop()
            del self.counter
