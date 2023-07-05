import threading
from attrdict import AttrDict
import json

from utils.parser import get_config
from utils.loop_exception import LoopException
from traffic_counter import TrafficCounter

import grpc
from google.protobuf import wrappers_pb2 as wrappers
from .proto import interface_pb2
from .proto import interface_pb2_grpc

class RouteGuideServicer(interface_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        self.background_thread = None
        self.JsonFlow = ""
        self.Progress = 0.0
        self.Output_Video_Path = ""

    def Init_Task(self, request, context):
        self.background_thread = threading.Thread(
            target=self.Run_Task, args=(self, request))
        self.Progress = 0
        self.background_thread.start()

        return wrappers.BoolValue(value=True)

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

    @staticmethod
    def Run_Task(servicer, request):
        try:
            print("Start running task", flush=True)
            # Build args
            args = AttrDict({
                "mode": {
                    interface_pb2.Parameter.STRAIGHT: "straight",
                    interface_pb2.Parameter.T_INTERSECTION: "t_intersection",
                    interface_pb2.Parameter.CROSS_INTERSECTION: "cross_intersection"
                }[request.Traffic_Mode],
                "detector_line_t": [
                    request.T.x1, request.T.y1,
                    request.T.x2, request.T.y2
                ],
                "detector_line_a": [
                    request.A.x1, request.A.y1,
                    request.A.x2, request.A.y2
                ],
                "detector_line_b": [
                    request.B.x1, request.B.y1,
                    request.B.x2, request.B.y2
                ],
                "detector_line_x": [
                    request.X.x1, request.X.y1,
                    request.X.x2, request.X.y2
                ],
                "detector_line_y": [
                    request.Y.x1, request.Y.y1,
                    request.Y.x2, request.Y.y2
                ],
                "stable_period": request.Stabilization_Period,
                "output_name": request.Output_Video_Path,
                "start_frame": request.Start_Frame,
                "end_frame": request.End_Frame,
                "use_cuda": True,
                "display": False,
                "save_path": "./output/",
                "frame_interval": 1
            })

            # Build config
            config = get_config()
            config.merge_from_file("./configs/yolov3.yaml")
            config.merge_from_file("./configs/deep_sort.yaml")
            config.USE_MMDET = False
            config.USE_DEEPSORT = True
            config.USE_FASTREID = True
            config.USE_OCSORT = False
            config.USE_BYTETRACK = False

            if config.USE_FASTREID:
                config.merge_from_file("./configs/fastreid.yaml")

            # Build Traffic counter
            counter = TrafficCounter(config, args, 
                video_path="./videos/" + request.Input_Video_Path)
            servicer.Output_Video_Path = request.Output_Video_Path + ".mp4"

            # Assume cross thread communication is safe
            counter.init_loop()
            while not servicer.background_thread is None:
                try:
                    servicer.Progress = counter.loop()
                except LoopException as e:
                    break
            
            # Finalize the loop
            if not counter is None:
                servicer.JsonFlow = json.dumps(counter.finalize_loop())
                del counter
        except Exception as e:
            print(str(e), flush=True)
        
        # Completed
        servicer.Progress = 1
