from flask import Flask, request, jsonify
from app import app
import subprocess
import os

from routes.rpc_controller.task_queue import TaskQueue

@app.route('/query_task', methods=['GET'])
def query_task():
    # Since RpcController is singleton, video_id is not necessary.
    video_id = request.args.get('videoId')

    task_info = TaskQueue.get_task_result(video_id)
    if task_info == None:
        return jsonify({ 
            "progress": 0,
            "flow": "",
            "independentFlow": "",
            "videoUrl": "",
            "state": "WAITING",
        })
    else:
        return jsonify({ 
            "progress": task_info["Progress"],
            "flow": task_info["Json_Flow"],
            "independentFlow": task_info["Independent_Results"],
            "videoUrl": task_info["Output_Video_Path"],
            "state": task_info["State"],
        })