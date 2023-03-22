import os
import subprocess
import copy
import cv2
from attrdict import AttrDict
import json
from queue import Queue

import time
import threading

from .proto import interface_pb2
from .client import RpcClient

# Singleton design to prevent multiple instances of the controller.
class RpcController:
    controller_state = "INIT"
    clients = []
    params = None
    config = {
        'UPLOAD_FOLDER': "/mnt/video-in/",
        'STATIC_URL': os.environ['BACKEND_HOST'] + "static/"
    }
    task_result = None
    pending_params = None

    @staticmethod
    def init_task(params):
        RpcController.completed = False
        RpcController.params = params
        RpcController.controller_state = "RUNNING"
        RpcController.task_result = {
            "Json_Flow": None,
            "Independent_Results": {},
            "Progress": 0,
            "Output_Video_Path": ""
        }

        # Initialize hosts
        host_list = os.environ["RPC_HOST_LIST"].split(",")
        for client in RpcController.clients:
            del client
        RpcController.clients = [RpcClient(host) for host in host_list]

        # Generate tasks
        total_frames = RpcController.get_video_frames(
            os.path.join(RpcController.config['UPLOAD_FOLDER'], params["Input_Video_Path"]))
        RpcController.pending_params = Queue()

        task_id = 0
        while task_id < RpcController.params["Slice_Count"]:
            new_params = copy.deepcopy(params)
            new_params["task_id"] = task_id
            new_params["Output_Video_Path"] = \
                params["Output_Video_Path"] + "-" + str(task_id)
            new_params["Start_Frame"] = task_id * total_frames // RpcController.params["Slice_Count"]
            new_params["End_Frame"] = (task_id + 1) * total_frames // RpcController.params["Slice_Count"]
            RpcController.pending_params.put_nowait(new_params)
            task_id += 1

        # Start the thread without waiting
        for i in range(len(host_list)):
            threading.Thread(target=RpcController.execute_task, args=(i,)).start()

    @staticmethod
    def execute_task(client_id):
        while not RpcController.pending_params.empty():
            param = RpcController.pending_params.get()
            print(f"[Executing params on client #{client_id}] ", param)

            client = RpcController.clients[client_id]

            client.Init_Task(param)
            while client.Get_State() != "COMPLETED":
                time.sleep(1)
            
            RpcController.task_result["Independent_Results"][param["task_id"]] = {
                "flow": json.loads(client.Get_Task().JsonFlow),
                "video_path": client.Get_Task().Output_Video_Path
            }

    @staticmethod
    def get_task():
        # Evaluate progress on the fly
        progress = RpcController.params["Slice_Count"] - RpcController.pending_params.qsize()
        for client in RpcController.clients:
            if client.Get_State() == "RUNNING":
                result = client.Get_Task()
                print(result)
                progress += result.Progress - 1
        RpcController.task_result["Progress"] = int(100 * progress) // RpcController.params["Slice_Count"]

        # Task become completed
        completed = len(RpcController.task_result["Independent_Results"]) == RpcController.params["Slice_Count"]
        become_complete = completed and RpcController.controller_state != "COMPLETED"     

        if become_complete:
            RpcController.controller_state = "COMPLETED"

            # Merge videos
            RpcController.merge_video([
                "/mnt/video-out/" + item["video_path"]
                for item in RpcController.task_result["Independent_Results"].values()])
            RpcController.task_result["Output_Video_Path"] = RpcController.config['STATIC_URL'] + \
                RpcController.params["Output_Video_Path"] + ".mp4"

            for task_id in RpcController.task_result["Independent_Results"]:
                result = RpcController.task_result["Independent_Results"][task_id]["flow"]
                RpcController.task_result["Json_Flow"] = RpcController.merge_json(
                    RpcController.task_result["Json_Flow"], result)

        return RpcController.task_result
        
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
            if type(x[key]) == dict:
                ans[key] = RpcController.merge_json(x[key], y[key])
            else:
                ans[key] = x[key] + y[key]
        return ans
    
    @staticmethod
    def merge_video(path_list):
        with open("/tmp/filelist.txt", "w+") as f:
           for path in path_list:
               f.write("file " + path + "\n")

        out_path = RpcController.params["Output_Video_Path"]
        result = subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", 
            "-i", "/tmp/filelist.txt", "-c", "copy", 
            f"/mnt/video-in/{out_path}.mp4"])
        print(result)

    @staticmethod
    def get_video_frames(filename):
        video = cv2.VideoCapture(filename)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        return frame_count