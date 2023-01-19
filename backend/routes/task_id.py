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
    mode = request.args.get('modeValue')
    detector = json.loads(request.args.get('detector'))

    args = ""
    if mode == 'straight':
        try:
            args += f"--detector_line {detector['T']['x1']},{detector['T']['y1']},{detector['T']['x2']},{detector['T']['y2']} "
        except:
            pass
    if mode == 't_intersection':
        try:
            args += f"--detector_line_t {detector['T']['x1']},{detector['T']['y1']},{detector['T']['x2']},{detector['T']['y2']} "
            args += f"--detector_line_a {detector['A']['x1']},{detector['A']['y1']},{detector['A']['x2']},{detector['A']['y2']} "
            args += f"--detector_line_b {detector['B']['x1']},{detector['B']['y1']},{detector['B']['x2']},{detector['B']['y2']} "
        except:
            pass
    if mode == 'cross_intersection':
        try:
            args += f"--detector_line_x {detector['X']['x1']},{detector['X']['y1']},{detector['X']['x2']},{detector['X']['y2']} "
            args += f"--detector_line_y {detector['Y']['x1']},{detector['Y']['y1']},{detector['Y']['x2']},{detector['Y']['y2']} "
            args += f"--detector_line_a {detector['A']['x1']},{detector['A']['y1']},{detector['A']['x2']},{detector['A']['y2']} "
            args += f"--detector_line_b {detector['B']['x1']},{detector['B']['y1']},{detector['B']['x2']},{detector['B']['y2']} "
        except:
            pass
    with open('scripts/init_task.sh', 'r') as file:
        bash_template = file.read()
        bash_command = bash_template.format(
            stabilization=stabilization,
            detector_args=args,
            video_id=video_id,
            output_id=video_id.replace(".", ""),
            LOCAL_IP=os.environ['LOCAL_IP'],
            uuid=task_id,
            mode=mode
        )
    # raise Exception(bash_command)
    out = subprocess.check_output(
        bash_command, 
        shell=True
    )
    out = out.decode('utf-8')
    print("[Out]", out)
    
    return jsonify({ "id": task_id })
