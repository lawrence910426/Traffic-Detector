from flask import Flask, request, jsonify
from app import app
import subprocess
import os

from routes.rpc_controller.controller import RpcController

@app.route('/query_task', methods=['GET'])
def query_task():
    # Since RpcController is singleton, video_id is not necessary.
    video_id = request.args.get('videoId')

    task_info = RpcController.get_task()
    return jsonify({ 
        "progress": task_info.Progress,
        "flow": task_info.JsonFlow,
        "videoUrl": task_info.Output_Video_Path
    })