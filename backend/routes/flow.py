from flask import Flask, request, jsonify
from app import app
import subprocess
import os
import json

@app.route('/flow', methods=['GET'])
def getFlow():
    task_id = request.args.get('taskId')
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
    raw_out = out = out.decode('utf-8')
    print("[Out]", out)
    
    try:
        out = out.split("\n")[1]
        flow = out.split("---")[0]
        flow = flow[6:-12]
        flow = flow.replace("\'", "\"")
        flow = json.loads(flow)
    except:
        raise Exception(raw_out)

    return flow
