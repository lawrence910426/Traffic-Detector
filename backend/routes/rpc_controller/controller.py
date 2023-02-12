import os
import subprocess
import copy
import cv2

from app import app

from .proto import interface_pb2
from .client import RpcClient

# Singleton design to prevent multiple instances of the controller.
class RpcController:
    controller_state = None
    clients = []
    params = None

    @staticmethod
    def init_task(params):
        RpcController.params = params
        RpcController.controller_state = "RUNNING"
        port_list = os.environ["RPC_PORT_LIST"].split(",")

        for client in RpcController.clients:
            del client
        RpcController.clients = [RpcClient(port) for port in port_list]

        total_frames = RpcController.get_video_frames(
            os.path.join(app.config['UPLOAD_FOLDER'], params["Input_Video_Path"]))
        for i in range(len(RpcController.clients)):
            new_params = copy.deepcopy(params)
            new_params["Output_Video_Path"] = \
                params["Output_Video_Path"] + "-" + str(i)
            new_params["Start_Frame"] = i * total_frames // len(RpcController.clients)
            new_params["End_Frame"] = (i + 1) * total_frames // len(RpcController.clients)
            RpcController.clients[i].Init_Task(new_params)

    @staticmethod
    def get_task():
        completed = True
        task_result = interface_pb2.TaskResult()
        task_result.JsonFlow = {}

        # Loop through the clients
        for client in RpcController.clients:
            completed = completed and client.Get_State() != "COMPLETED"
            result = client.Get_Task()
            task_result.Progress += result.Progress
            RpcController.merge_json(task_result.JsonFlow, result.JsonFlow)
        task_result.Progress = 100 * task_result.Progress // len(RpcController.clients)
        
        # Merge all videos into one big video
        video_list = [
            "/mnt/video-out/" + client.Get_Task().Output_Video_Path
            for client in RpcController.clients]

        # Task become completed        
        if completed and RpcController.controller_state != "COMPLETED":
            RpcController.merge_video(video_list)
            RpcController.clients = []
            RpcController.controller_state = "COMPLETED"

        # Generate the output video url if completed
        if completed:            
            task_result.Output_Video_Path = app.config['STATIC_URL'] + "/" + \
                RpcController.params["Output_Video_Path"]
        return task_result
        
    @staticmethod
    def kill_task():
        for client in RpcController.clients:
            del client
        RpcController.clients = []
        RpcController.controller_state = "COMPLETED"

    @staticmethod
    def get_state():
        return RpcController.controller_state
    
    @staticmethod
    def merge_json(x, y):
        if x is None:
            return y
        if y is None:
            return x
        
        ans = {}
        for key in x:
            if type(x[key]) == int:
                ans[key] = x[key] + y[key]
            else:
                ans[key] = RpcController.merge_json(x[key], y[key])
        return ans
    
    @staticmethod
    def merge_video(path_list):
        with open("/tmp/filelist.txt", "w+") as f:
           for path in path_list:
               f.write("file " + path)

        out_path = RpcController.params["Output_Video_Path"]
        result = subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", 
            "-i", "/tmp/filelist.txt", "-c", "copy", 
            f"/mnt/video-out/{out_path}.mp4"])
        print(result)

    @staticmethod
    def get_video_frames(filename):
        video = cv2.VideoCapture(filename)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        return frame_count