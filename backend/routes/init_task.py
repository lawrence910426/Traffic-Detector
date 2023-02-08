from flask import Flask, request, jsonify
from app import app
import subprocess
import json
import os
import uuid
from ..rpc_controller import RpcController

@app.route('/init_task', methods=['GET'])
def init_task():
    video_id = request.args.get('id')
    stabilization = request.args.get('stabilization')
    mode = request.args.get('modeValue')
    detector = json.loads(request.args.get('detector'))

    unique_id = video_id.split(".")[0]
    params = {
        "Mode": mode,
        "Stabilization_Period": stabilization,
        "Input_Video_Path": f"input/{video_id}",
        "Output_Video_Path": f"output/{unique_id}",
        "X": detector['X'],
        "Y": detector['Y'],
        "T": detector['T'],
        "A": detector['A'],
        "B": detector['B']
    }
    RpcController.init_task(params)
    
    return jsonify({ "id": unique_id })
