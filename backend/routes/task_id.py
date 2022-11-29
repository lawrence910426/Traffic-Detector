from flask import Flask, request, jsonify
from app import app
import subprocess
import json
import os
import uuid

@app.route('/task_id', methods=['GET'])
def getTaskId():
    task_id = uuid.uuid4()
    video_id = request.args.get('id')
    stabilization = request.args.get('stabilization')
    detector = json.loads(request.args.get('detector'))
    detector = f"{detector['x1']},{detector['y1']},{detector['x2']},{detector['y2']}"

    with open('scripts/init_task.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            stabilization=stabilization,
            detector=detector,
            video_id=video_id,
            output_id=video_id.replace(".", ""),
            LOCAL_IP=os.environ['LOCAL_IP'],
            uuid=task_id
        )
    # raise Exception(bash_command)
    out = subprocess.check_output(
        bash_command, 
        shell=True
    )
    out = out.decode('utf-8')
    print("[Out]", out)

    out = out.split("\n")[-3]
    return jsonify({ "id": task_id })
