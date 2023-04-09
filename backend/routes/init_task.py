from flask import Flask, request, jsonify
from app import app
import subprocess
import json
import os
import uuid
import sys

from routes.rpc_controller.task_queue import TaskQueue

@app.route('/init_task', methods=['GET'])
def init_task():
    video_id = request.args.get('id')
    stabilization = request.args.get('stabilization')
    mode = request.args.get('modeValue')
    detector = json.loads(request.args.get('detector'))
    null_detector = { "x1": 0, "y1": 0, "x2": 0, "y2": 0 }
    slices = int(request.args.get('slice'))

    unique_id = str(uuid.uuid4())
    params = {
        "Mode": mode,
        "Stabilization_Period": stabilization,
        "Input_Video_Path": f"{video_id}",
        "Output_Video_Path": f"{unique_id}",
        "Slice_Count": slices,
        "X": detector['X'] if 'X' in detector else null_detector,
        "Y": detector['Y'] if 'Y' in detector else null_detector,
        "T": detector['T'] if 'T' in detector else null_detector,
        "A": detector['A'] if 'A' in detector else null_detector,
        "B": detector['B'] if 'B' in detector else null_detector
    }
    TaskQueue.add_task(params)
    
    return jsonify({ "id": unique_id })
