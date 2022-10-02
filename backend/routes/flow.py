from flask import Flask, request, jsonify
from app import app
import subprocess
import os
import json

@app.route('/flow', methods=['GET'])
def getFlow():
    task_id = request.args.get('taskId')
    
    # First, upload the video
    with open('scripts/get_result_vdo.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            id=task_id,
            host=os.environ['BACKEND_HOST'],
            LOCAL_IP=os.environ['LOCAL_IP']
        )
    out = subprocess.check_output(
        bash_command, 
        shell=True
    )
    out = out.decode('utf-8')
    print("[Out]", out)

    out = out.split("\n")[1]
    url = json.loads(out)["url"]

    # Next, get the traffic flow
    with open('scripts/get_result_flow.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            id=task_id,
            LOCAL_IP=os.environ['LOCAL_IP']
        )

    out = subprocess.check_output(
        bash_command, 
        shell=True
    )
    out = out.decode('utf-8')
    print("[Out]", out)
    
    out = out.split("\n")[1]
    flow = out.split("---")[-1]

    # Last, combine the results
    flow = json.loads(flow)
    flow.videoUrl = url
    return flow
